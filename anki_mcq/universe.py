#!/usr/bin/env python3
"""
anki_mcq.universe - Safe, generalized deduplication-universe builder.

WHAT THIS DOES
--------------
Builds the "already-studied universe" for the dedupe pipeline by taking the UNION
of two sources of truth:

  1. LOCAL   - a JSON store in the repo (decks/<exam>/dedupe/universe_cards.json)
  2. ANKI    - the live collection, read via AnkiConnect (localhost:8765)

An LLM classifies which Anki decks are cloud/software-certification related
(vs. noise like languages, religion, accounting) so we NEVER assume an unstudied
deck is "already known". Sync is STRICTLY ONE-WAY (Anki -> local): relevant decks
found in Anki are downloaded into the local universe, but NOTHING is ever written,
modified, or deleted in Anki.

SAFETY (structural, not by convention)
--------------------------------------
`invoke()` here uses an ALLOWLIST of read-only AnkiConnect actions
(version, deckNames, findNotes, notesInfo). Any other action raises immediately.
This module deliberately does NOT import the mutating engine/sync code, so there
is no code path from here to addNote/updateNoteFields/deleteNotes/createModel.

IDENTITY MODEL (settled by investigations d6af44d1 + v2-b806e0)
---------------------------------------------------------------
`notesInfo` does not expose a GUID, so genanki GUIDs are never used for matching.
Each note gets a stable identity:

  * mcqkey  - for engine-generated notes carrying a hidden tag
              `mcqkey:<sha1(key or question)[:16]>` (written by sync_deck).
              This hash is over the RAW (un-normalized) text.
  * qhash   - for everything else (foreign models: SAP-C02, CCNA, Docker, ...).
              `sha1(normalize(question_field))[:16]`, where the question field is
              chosen by a MODEL-AWARE priority list (never "first field", which
              would collapse e.g. all 884 CCNA notes onto the `Author` field).

Cards are unioned with a multi-key union-find index: two records merge if they
share ANY key, EXCEPT we refuse to bridge two DISTINCT mcqkeys (that would chain
unrelated concepts) - such conflicts are logged, not merged.

OUTPUT
------
  * universe_cards.json  - the full audit store (id_kind, id16, deck, source, ...)
  * existing_cards.json  - the CONSUMER file that prepare_concepts.py already
                           reads (schema: note_id, query, question, options).
                           Written so prepare_concepts.py runs UNMODIFIED.
"""
import datetime
import hashlib
import json
import os
import re
import urllib.request

ANKICONNECT = "http://localhost:8765"
KEY_TAG_PREFIX = "mcqkey:"

# Only these read-only actions are permitted. Anything else raises.
_ALLOWED_ACTIONS = frozenset({"version", "deckNames", "deckNamesAndIds",
                              "findNotes", "notesInfo"})

# Model-aware question-field priority. First present, non-empty field wins.
# Order matters: it is the join key for foreign-model decks. Do NOT rely on
# Anki field insertion order (not a documented contract) - hence this explicit
# list, with a dict-order fallback only for un-enumerated models.
QFIELD_PRIORITY = ("Front", "Question", "Text", "Note", "Highlight")
# Fields to treat as "options / answer / context" for the consumer's options str.
OFIELD_PRIORITY = ("OptionsQ", "OptionsA", "Options", "Back", "Answer",
                   "Comments", "Extra", "Highlight")


class AnkiWriteAttempt(RuntimeError):
    """Raised if any non-allowlisted (potentially mutating) action is invoked."""


class AnkiUnreachable(RuntimeError):
    """Raised when AnkiConnect cannot be reached - we fail loud, never silent."""


class SystemicNotesInfoFailure(RuntimeError):
    """Raised when notesInfo fails repeatedly (circuit-breaker tripped)."""


# --------------------------------------------------------------------------- #
# AnkiConnect (READ-ONLY)
# --------------------------------------------------------------------------- #
def invoke(action, _endpoint=ANKICONNECT, **params):
    """Call AnkiConnect, but STRUCTURALLY refuse anything not on the allowlist."""
    if action not in _ALLOWED_ACTIONS:
        raise AnkiWriteAttempt(
            f"Refused non-read-only AnkiConnect action '{action}'. "
            f"universe.py is one-way (Anki -> local) and may only call "
            f"{sorted(_ALLOWED_ACTIONS)}.")
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(_endpoint, data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise AnkiUnreachable(
            f"AnkiConnect unreachable at {_endpoint}: {e}. "
            f"Open Anki with the AnkiConnect add-on and retry.") from e
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect '{action}': {data['error']}")
    return data["result"]


# --------------------------------------------------------------------------- #
# Text normalization + hashing
# --------------------------------------------------------------------------- #
_CLOZE_RE = re.compile(r"\{\{c\d+::(.*?)(?:::.*?)?\}\}", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_ENT_RE = re.compile(r"&[a-z]+;")
_WS_RE = re.compile(r"\s+")


def strip_cloze(s):
    """Replace Anki cloze markup {{c1::answer::hint}} with just 'answer'."""
    return _CLOZE_RE.sub(lambda m: m.group(1), s or "")


def strip_html(s):
    """Strip HTML tags + &entities;. Does NOT touch cloze markup (identity-safe)."""
    s = _TAG_RE.sub(" ", s or "")
    s = _ENT_RE.sub(" ", s)
    return _WS_RE.sub(" ", s).strip()


def normalize(s, cloze=False):
    """Normalize for IDENTITY or JUDGE text.

    cloze=False (default, IDENTITY path): keep cloze braces intact so the hash is
        stable regardless of how the judge later renders the card.
    cloze=True (JUDGE/concept path only): also strip cloze markup for readability.
    """
    if cloze:
        s = strip_cloze(s)
    return strip_html(s).lower().strip()


def sha16(s):
    """16 hex chars of sha1 - the identity primitive used everywhere."""
    return hashlib.sha1((s or "").encode("utf-8")).hexdigest()[:16]


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- #
# Field selection + identity extraction
# --------------------------------------------------------------------------- #
def pick_question_field(fields):
    """Return the name of the question field via the model-aware priority list.

    `fields` is the AnkiConnect notesInfo fields dict: {name: {value, order}}.
    Falls back to the first non-empty field (dict order) only for models whose
    fields are none of QFIELD_PRIORITY.
    """
    for name in QFIELD_PRIORITY:
        v = fields.get(name)
        if v and v.get("value", "").strip():
            return name
    for name, v in fields.items():
        if v.get("value", "").strip():
            return name
    return None


def pick_options_field(fields, exclude):
    """Return concatenated text of the FIRST matching options/answer field.

    Only ONE field is used (fixes the historical double-append bug where both
    OptionsQ and OptionsA were concatenated).
    """
    for name in OFIELD_PRIORITY:
        if name == exclude:
            continue
        v = fields.get(name)
        if v and v.get("value", "").strip():
            return v["value"]
    return ""


def extract_id(note):
    """Return (id_kind, id16) for an Anki note.

    mcqkey (from tag) wins; otherwise qhash over the normalized question field.
    Returns (None, None) for a malformed/empty note (caller skips + logs).
    """
    for tag in note.get("tags", []):
        if tag.startswith(KEY_TAG_PREFIX):
            val = tag[len(KEY_TAG_PREFIX):].strip()
            if val:
                return "mcqkey", val
    fields = note.get("fields", {})
    qname = pick_question_field(fields)
    if not qname:
        return None, None
    return "qhash", sha16(normalize(fields[qname]["value"]))


# --------------------------------------------------------------------------- #
# Multi-key union-find over card records
# --------------------------------------------------------------------------- #
def _record_keys(rec):
    """All lookup keys a record can be found under.

    - Anki note:  its own (id_kind:id16), plus qhash of its question.
    - Local engine card: qhash of its question, plus mcqkey:sha16(raw_key) and
      mcqkey:sha16(raw_question) (RAW bytes, matching sync_deck._key_tag), so it
      matches the same card sitting in Anki under either identity.
    NEVER emits sha16("") - an empty key contributes no mcqkey alias.
    """
    keys = set()
    if rec.get("id_kind") and rec.get("id16"):
        keys.add(f"{rec['id_kind']}:{rec['id16']}")
    q = rec.get("question")
    if q:
        keys.add(f"qhash:{sha16(normalize(q))}")
    rk = rec.get("raw_key")
    if rk:
        keys.add(f"mcqkey:{sha16(rk)}")
    rq = rec.get("raw_question")
    if rq:
        # RAW bytes (no normalize) - matches how sync_deck hashed the card.
        keys.add(f"mcqkey:{sha16(rq)}")
    return keys


def _authoritative_mcqkey(rec):
    """The single authoritative mcqkey for a record, or None.

    Authoritative = the note's own stable engine key: the mcqkey tag (id16 when
    id_kind==mcqkey) or sha16(raw_key). A raw_question-derived mcqkey is only a
    soft cross-source *alias* for matching, NOT an authoritative identity, so it
    must NOT count toward "distinct concepts bridged".
    """
    if rec.get("id_kind") == "mcqkey" and rec.get("id16"):
        return "mcqkey:" + rec["id16"]
    if rec.get("raw_key"):
        return "mcqkey:" + sha16(rec["raw_key"])
    return None


def _distinct_mcqkeys(recs):
    """Distinct AUTHORITATIVE mcqkeys across records (chain-risk discriminator)."""
    out = set()
    for r in recs:
        mk = _authoritative_mcqkey(r)
        if mk:
            out.add(mk)
    return out


def _merge_two(a, b):
    """Merge b into a. Prefer live Anki text; union provenance."""
    out = dict(a)
    # source: anki + local -> both
    sa, sb = a.get("source"), b.get("source")
    out["source"] = "both" if (sa and sb and sa != sb) else (sa or sb)
    # prefer Anki (live) question/options text
    if sb == "anki":
        out["question"] = b.get("question") or a.get("question")
        out["options"] = b.get("options") or a.get("options")
    else:
        out["question"] = a.get("question") or b.get("question")
        out["options"] = a.get("options") or b.get("options")
    # mcqkey identity is authoritative over qhash
    if a.get("id_kind") == "mcqkey":
        out["id_kind"], out["id16"] = a["id_kind"], a["id16"]
    elif b.get("id_kind") == "mcqkey":
        out["id_kind"], out["id16"] = b["id_kind"], b["id16"]
    else:
        out["id_kind"] = a.get("id_kind") or b.get("id_kind")
        out["id16"] = a.get("id16") or b.get("id16")
    out["raw_key"] = a.get("raw_key") or b.get("raw_key")
    out["raw_question"] = a.get("raw_question") or b.get("raw_question")
    out["mod"] = max(a.get("mod") or 0, b.get("mod") or 0) or None
    # keep the first-seen deck/deck_root/note_id/query for provenance
    for f in ("deck", "deck_root", "note_id", "query", "surrogate_id"):
        out[f] = a.get(f) if a.get(f) not in (None, "") else b.get(f)
    return out


def union_cards(records, conflicts_out=None):
    """Union a list of card records by multi-key matching.

    Returns the deduplicated list. Refuses to bridge >=2 distinct mcqkeys
    (logs to conflicts_out list instead of merging).
    """
    index = {}          # key -> record (current representative)
    conflicts = conflicts_out if conflicts_out is not None else []

    for rec in records:
        rec = dict(rec)
        keys = _record_keys(rec)
        # find existing representatives this record touches
        hits = []
        seen = set()
        for k in keys:
            r = index.get(k)
            if r is not None and id(r) not in seen:
                hits.append(r)
                seen.add(id(r))
        if not hits:
            for k in keys:
                index[k] = rec
            continue
        # would merging bridge >=2 distinct mcqkeys?
        candidate_group = hits + [rec]
        if len(_distinct_mcqkeys(candidate_group)) >= 2:
            conflicts.append({
                "reason": ">=2 distinct mcqkeys would be bridged; not merged",
                "incoming": {kk: rec.get(kk) for kk in ("id_kind", "id16", "deck",
                             "note_id", "raw_key")},
                "existing_mcqkeys": sorted(_distinct_mcqkeys(hits)),
            })
            # register the incoming record only under keys not already owned
            for k in keys:
                index.setdefault(k, rec)
            continue
        # safe merge: fold all hits + rec into one representative
        merged = rec
        for h in hits:
            merged = _merge_two(merged, h)
        for k in _record_keys(merged):
            index[k] = merged

    # dedupe representatives by object identity
    uniq = {}
    for r in index.values():
        uniq[id(r)] = r
    return list(uniq.values())


# --------------------------------------------------------------------------- #
# Anki census (READ-ONLY) with circuit-breaker
# --------------------------------------------------------------------------- #
def _notes_info_resilient(note_ids, endpoint=ANKICONNECT, breaker=5):
    """notesInfo for many ids: batch of 100, degrade to per-id, index by noteId.

    Trips a circuit-breaker after `breaker` consecutive per-id failures
    (systemic AnkiConnect fault) and aborts loudly.
    """
    by_id = {}
    consecutive = 0
    for i in range(0, len(note_ids), 100):
        batch = note_ids[i:i + 100]
        try:
            infos = invoke("notesInfo", _endpoint=endpoint, notes=batch)
            for info in infos:
                if info:                      # {} => deleted id, skip
                    by_id[info["noteId"]] = info
            consecutive = 0
            continue
        except Exception:
            pass  # fall through to per-id
        for nid in batch:
            try:
                infos = invoke("notesInfo", _endpoint=endpoint, notes=[nid])
                info = infos[0] if infos else None
                if info:
                    by_id[info["noteId"]] = info
                consecutive = 0
            except Exception:
                consecutive += 1
                if consecutive >= breaker:
                    raise SystemicNotesInfoFailure(
                        f"notesInfo failed {consecutive} times in a row - "
                        f"systemic AnkiConnect fault. Aborting; nothing written.")
    return by_id


def census_relevant_notes(relevant_roots, endpoint=ANKICONNECT):
    """Pull all notes from the relevant deck roots. Returns (records, skipped)."""
    records, skipped = [], []
    for root in relevant_roots:
        query = f'deck:"{root}" OR deck:"{root}::*"'
        ids = invoke("findNotes", _endpoint=endpoint, query=query)
        if not ids:
            continue
        by_id = _notes_info_resilient(ids, endpoint=endpoint)
        for nid in ids:
            info = by_id.get(nid)
            if not info:
                continue
            id_kind, id16 = extract_id(info)
            fields = info.get("fields", {})
            qname = pick_question_field(fields)
            if not id16 or not qname:
                skipped.append({"noteId": nid, "reason": "no question field / empty"})
                continue
            q_raw = fields[qname]["value"]
            q_clean = strip_html(q_raw)
            if not q_clean:
                # e.g. image-only or blank <br> cards: no dedupable text
                skipped.append({"noteId": nid, "reason": "question empty after strip_html"})
                continue
            opts_raw = pick_options_field(fields, exclude=qname)
            records.append({
                "id_kind": id_kind,
                "id16": id16,
                "raw_key": None,
                "raw_question": None,
                "note_id": nid,
                "deck": root,
                "deck_root": root,
                "query": f'deck:"{root}::*"',
                "question": q_clean,
                "options": strip_html(opts_raw),
                "concept": None,
                "mod": info.get("mod"),
                "source": "anki",
            })
    return records, skipped


# --------------------------------------------------------------------------- #
# Local store
# --------------------------------------------------------------------------- #
def load_local_universe(universe_path):
    """Load an existing universe_cards.json (its `cards` list), or []."""
    if not os.path.exists(universe_path):
        return []
    data = json.loads(open(universe_path, encoding="utf-8").read())
    return data.get("cards", [])


def local_cards_from_engine(cards, deck_root):
    """Convert engine card() dicts (with 'key'/'question') into universe records.

    Used to seed the local source of truth from a deck's generator script.
    """
    out = []
    for c in cards:
        rk = c.get("key")
        rq = c["question"]
        out.append({
            "id_kind": "mcqkey" if rk else "qhash",
            "id16": sha16(rk) if rk else sha16(normalize(rq)),
            "raw_key": rk,
            "raw_question": rq,               # RAW bytes for identity match
            "note_id": None,
            "surrogate_id": "local:" + sha16(rk or rq),
            "deck": deck_root,
            "deck_root": deck_root,
            "query": "",
            "question": strip_html(rq),
            "options": "",
            "concept": None,
            "mod": None,
            "source": "local",
        })
    return out


def _atomic_write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def write_universe(universe_path, cards):
    counts = {
        "local": sum(1 for c in cards if c.get("source") == "local"),
        "anki": sum(1 for c in cards if c.get("source") == "anki"),
        "both": sum(1 for c in cards if c.get("source") == "both"),
    }
    qhash_only = sum(1 for c in cards if c.get("id_kind") == "qhash")
    out = {
        "generated_at": now_iso(),
        "sources": {**counts, "union": len(cards)},
        "qhash_only_count": qhash_only,
        "cards": cards,
    }
    _atomic_write(universe_path, json.dumps(out, ensure_ascii=False, indent=2))
    return out


def write_consumer_existing_cards(existing_path, cards):
    """Write existing_cards.json in the schema prepare_concepts.py consumes.

    Consumer reads: c['note_id'], c.get('query'), c['question'], c.get('options').
    All present here; extra keys are ignored by the consumer.
    """
    rows = []
    for c in cards:
        rows.append({
            "note_id": c.get("note_id"),
            "query": c.get("query") or "",
            "question": c.get("question") or "",
            "options": c.get("options") or "",
            # provenance-only extras (consumer ignores):
            "id_kind": c.get("id_kind"),
            "id16": c.get("id16"),
            "deck": c.get("deck"),
            "source": c.get("source"),
        })
    _atomic_write(existing_path, json.dumps(rows, ensure_ascii=False, indent=2))
    return rows



# --------------------------------------------------------------------------- #
# Top-level orchestrator
# --------------------------------------------------------------------------- #
def get_deck_roots(endpoint=ANKICONNECT):
    """Return sorted unique top-level deck roots from Anki (READ-ONLY)."""
    names = invoke("deckNames", _endpoint=endpoint)
    return sorted({n.split("::")[0] for n in names})


def build_universe(exam_dir, allowlist_path=None, classify_fn=None,
                   endpoint=ANKICONNECT, extra_local_cards=None):
    """Build the dedup universe = UNION(local JSON, relevant Anki decks).

    ONE-WAY: reads Anki (read-only), writes ONLY local files. Never mutates Anki.

    Parameters
    ----------
    exam_dir : path to decks/<exam>/dedupe/
    allowlist_path : path to relevant_decks.json (defaults to repo-root shared
        file if it exists, else exam_dir/relevant_decks.json).
    classify_fn : callable(roots)->verdicts for NEW roots. Defaults to the
        deterministic heuristic (see deck_classifier). The agent may pass an
        LLM-backed callable.
    extra_local_cards : optional list of engine card() dicts to fold into the
        local source of truth (converted via local_cards_from_engine).

    Returns a summary dict.
    """
    from .deck_classifier import build_relevant_decks, heuristic_classify, relevant_roots

    exam_dir = os.path.abspath(exam_dir)
    universe_path = os.path.join(exam_dir, "universe_cards.json")
    existing_path = os.path.join(exam_dir, "existing_cards.json")
    conflicts_path = os.path.join(exam_dir, "universe_conflicts.json")
    skipped_path = os.path.join(exam_dir, "universe_skipped.json")

    if allowlist_path is None:
        repo_shared = _find_repo_root_allowlist(exam_dir)
        allowlist_path = repo_shared or os.path.join(exam_dir, "relevant_decks.json")
    if classify_fn is None:
        classify_fn = heuristic_classify

    # 1. discover + classify deck roots (cached, pinned-aware)
    roots = get_deck_roots(endpoint=endpoint)
    allow = build_relevant_decks(roots, allowlist_path, classify_fn=classify_fn)
    rroots = relevant_roots(allow)

    # 2. load local source of truth
    local = load_local_universe(universe_path)
    for c in local:
        c.setdefault("source", "local")
    if extra_local_cards:
        # infer deck_root from the first relevant root or leave generic
        local += local_cards_from_engine(extra_local_cards,
                                          deck_root=(rroots[0] if rroots else "local"))

    # 3. census Anki relevant decks (READ-ONLY)
    anki_records, skipped = census_relevant_notes(rroots, endpoint=endpoint)

    # 4. UNION + dedup (multi-key union-find, conflict-safe)
    conflicts = []
    universe = union_cards(local + anki_records, conflicts_out=conflicts)

    # 5. persist (atomic). Never touches Anki.
    uni = write_universe(universe_path, universe)
    write_consumer_existing_cards(existing_path, universe)
    if conflicts:
        _atomic_write(conflicts_path, json.dumps(conflicts, ensure_ascii=False, indent=2))
    if skipped:
        _atomic_write(skipped_path, json.dumps(skipped, ensure_ascii=False, indent=2))

    return {
        "roots_total": len(roots),
        "relevant_roots": rroots,
        "anki_notes": len(anki_records),
        "local_cards": len(local),
        "union": len(universe),
        "conflicts": len(conflicts),
        "skipped": len(skipped),
        "qhash_only": uni["qhash_only_count"],
        "allowlist_path": allowlist_path,
        "universe_path": universe_path,
        "existing_cards_path": existing_path,
    }


def _find_repo_root_allowlist(start_dir):
    """Walk up from exam_dir looking for a repo-root relevant_decks.json.

    Returns its path if a repo root (has pyproject.toml or .git) contains one,
    else None. This lets all exams share a single global allowlist.
    """
    d = os.path.abspath(start_dir)
    while True:
        if (os.path.exists(os.path.join(d, "pyproject.toml"))
                or os.path.isdir(os.path.join(d, ".git"))):
            cand = os.path.join(d, "relevant_decks.json")
            return cand if os.path.exists(cand) else None
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent
