"""Angry Judge: The Short Rant Contest.

Writes one short, funny rant about an everyday annoyance
(a late bus) to /output/entry.txt.
"""

import os
import sys

ENTRY = (
    "The bus was due at 8:04. It arrived at 8:47, smug as a cat, "
    "flashing NOT IN SERVICE. Then three buses came at once, like "
    "buses do -- because apparently they travel in packs, and the "
    "first one is just a scout. I stood in the rain for "
    "forty-three minutes while the app said 'arriving now'. It "
    "lied. It watched me get wet, and it lied."
)


def resolve_output_path():
    if os.environ.get("ENTRY_OUTPUT"):
        return os.environ["ENTRY_OUTPUT"]
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    return "/output/entry.txt"


def main():
    text = ENTRY
    if not text.strip():
        print("error: entry text is empty or only whitespace", file=sys.stderr)
        return 1
    if len(text) > 400:
        print(
            "error: entry text is %d characters, over the 400 limit"
            % len(text),
            file=sys.stderr,
        )
        return 1
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != text.encode("utf-8"):
        print(
            "error: read-back verification failed: %d bytes on disk "
            "differ from the %d bytes written" % (len(written), len(text)),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
