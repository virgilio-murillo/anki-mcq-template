#!/usr/bin/env python3
"""
Import a .apkg into a running Anki via the AnkiConnect add-on.

Prerequisites:
- Anki running with the AnkiConnect add-on (code 2055492159) installed.
- AnkiConnect listening on http://localhost:8765 (default).

Usage:
    ./.venv/bin/python import_to_anki.py example_deck.apkg
"""
import json
import os
import sys
import urllib.request

ANKICONNECT = "http://localhost:8765"


def invoke(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(ANKICONNECT, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect error on '{action}': {data['error']}")
    return data["result"]


def main():
    if len(sys.argv) != 2:
        print("usage: import_to_anki.py <deck.apkg>", file=sys.stderr)
        sys.exit(2)
    apkg = os.path.abspath(sys.argv[1])
    if not os.path.isfile(apkg):
        print(f"file not found: {apkg}", file=sys.stderr)
        sys.exit(1)
    try:
        ok = invoke("importPackage", path=apkg)
    except Exception as e:  # noqa: BLE001
        print(f"Could not reach AnkiConnect at {ANKICONNECT}. Is Anki open with the add-on? ({e})",
              file=sys.stderr)
        sys.exit(1)
    print(f"importPackage -> {ok}")
    print("Done. Check your Anki deck list (you may need to refresh the view).")


if __name__ == "__main__":
    main()
