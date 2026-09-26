#!/usr/bin/env python3
"""
anki_mcq.deck_classifier - Decide which Anki deck roots are cloud/software-cert
relevant (vs noise) for the dedup universe.

DESIGN (settled by investigation v2-b806e0, Dispute 5)
------------------------------------------------------
- The AUTHORITATIVE decision is made by an LLM judging deck names by MEANING,
  never by a naming pattern. The verdict is CACHED in relevant_decks.json.
- Governance per deck: {deck, relevant, confidence, review, rationale, pinned}.
  * pinned=true entries are frozen and never re-evaluated (user override).
  * A newly-seen root (not in the cached snapshot) is marked review=true.
- Borderline policy (policy.borderline_default): the user's forbidden failure is
  HIDING a genuinely-new question. Wrong-EXCLUDE only yields a visible, recoverable
  duplicate; wrong-INCLUDE can hide a new question. So the safe borderline default
  is "exclude". This is stored in the file and is user-overridable.

The LLM call itself is done by the agent/caller (there is no network LLM client
in this repo). `build_relevant_decks()` therefore takes a `classify_fn` callable:

    classify_fn(list_of_root_names) -> list of {deck, relevant, confidence,
                                                review, rationale}

For offline/testing, `heuristic_classify` provides a deterministic fallback
(keyword allow/deny hints). It is NOT the decider in production - it exists so the
pipeline is runnable and testable without a live LLM, and to cross-check the LLM.
"""
import json
import os

from .universe import now_iso

# The exact prompt the agent/LLM should use (temperature 0). Kept here so it is
# version-controlled and reused verbatim.
CLASSIFIER_PROMPT = """\
You are classifying Anki deck names to build a deduplication universe for a
CLOUD / SOFTWARE CERTIFICATION study tool (AWS, Azure, GCP, Kubernetes, Docker,
networking, Linux, security, databases, DevOps, and related IT certifications).

For EACH deck name below decide relevant=true if its content is about cloud
computing, software engineering, IT infrastructure, networking, DevOps, security,
databases, or a technical certification - content that could overlap with
cloud/software cert practice questions. Otherwise relevant=false (human languages,
religion, accounting, music, personal, "Default", or anything not technical-IT).

Judge by MEANING, not by naming pattern.
RELEVANT examples: "Docker", "CCNA 200-301", "Networking Fundamentals",
"AWS SAP-C02 - Improved Study Deck", "SAW", "MLA-C01", "DVA-C02".
NOISE examples: "Koine Griego", "biblia", "contabilidad", "Default".

When genuinely unsure, set relevant=false and review=true. A wrongly-included
non-studied deck could hide good new questions - that is the worse error.

Deck roots to classify (one per line):
{DECK_ROOTS}

Return ONLY a JSON array, no prose:
[{{"deck":"<exact name>","relevant":true|false,"confidence":0.0-1.0,"review":true|false,"reason":"<=12 words"}}]
"""

# Deterministic fallback hints (NOT the production decider).
_ALLOW_HINTS = ("aws", "azure", "gcp", "cloud", "kubernetes", "k8s", "docker",
                "container", "terraform", "devops", "security", "sql", "database",
                "network", "networking", "ccna", "cisco", "linux", "python",
                "java", "cert", "saa", "sap", "dva", "mla", "soa", "clf",
                "sysops", "developer", "architect", "saw")
_DENY_HINTS = ("biblia", "griego", "gri/ego", "koine", "koin", "contabilidad",
               "espanol", "espa", "ingles", "kanji", "hsk", "vocab", "verbos",
               "guitar", "music", "history", "geograf", "default")


def heuristic_classify(roots):
    """Deterministic keyword classifier. Fallback / cross-check only."""
    out = []
    for name in roots:
        low = name.lower()
        allow = any(h in low for h in _ALLOW_HINTS)
        deny = any(h in low for h in _DENY_HINTS)
        if allow and not deny:
            rel, conf, review = True, 0.9, False
        elif deny and not allow:
            rel, conf, review = False, 0.9, False
        else:
            # genuinely unsure -> safe default (exclude) + flag for review
            rel, conf, review = False, 0.3, True
        out.append({"deck": name, "relevant": rel, "confidence": conf,
                    "review": review, "reason": "keyword heuristic"})
    return out


def load_allowlist(path):
    if not os.path.exists(path):
        return None
    return json.loads(open(path, encoding="utf-8").read())


def build_relevant_decks(roots, path, classify_fn=heuristic_classify,
                         borderline_default="exclude"):
    """Build/refresh relevant_decks.json.

    - Only re-classifies roots NOT already present (diff against snapshot),
      preserving pinned entries verbatim.
    - Applies the borderline policy: a review=true / low-confidence deck follows
      policy.borderline_default unless pinned.
    Returns the allowlist dict.
    """
    prev = load_allowlist(path)
    prev_decks = {d["deck"]: d for d in prev["decks"]} if prev else {}
    policy_default = (prev.get("policy", {}).get("borderline_default")
                      if prev else None) or borderline_default

    known = set(prev_decks)
    new_roots = [r for r in roots if r not in known]

    verdicts = {}
    if new_roots:
        for v in classify_fn(new_roots):
            verdicts[v["deck"]] = v

    merged = {}
    for name in roots:
        if name in prev_decks and prev_decks[name].get("pinned"):
            merged[name] = prev_decks[name]           # frozen
            continue
        v = verdicts.get(name) or prev_decks.get(name)
        if v is None:
            # shouldn't happen, but be safe: treat as unseen/borderline
            v = {"deck": name, "relevant": False, "confidence": 0.0,
                 "review": True, "reason": "unclassified"}
        relevant = bool(v.get("relevant"))
        review = bool(v.get("review"))
        # borderline (flagged for review) follows policy default unless pinned
        if review and policy_default == "exclude":
            relevant = False
        elif review and policy_default == "include":
            relevant = True
        merged[name] = {
            "deck": name,
            "relevant": relevant,
            "confidence": v.get("confidence", 0.5),
            "review": review,
            "reason": v.get("reason", ""),
            "pinned": prev_decks.get(name, {}).get("pinned", False),
        }

    allow = {
        "generated_at": now_iso(),
        "policy": {"borderline_default": policy_default},
        "deck_roots_snapshot": sorted(roots),
        "decks": [merged[n] for n in sorted(merged)],
    }
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(allow, ensure_ascii=False, indent=2))
    os.replace(tmp, path)
    return allow


def relevant_roots(allow):
    return [d["deck"] for d in allow["decks"] if d.get("relevant")]
