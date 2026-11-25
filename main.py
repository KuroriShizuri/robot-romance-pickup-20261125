#!/usr/bin/env python3
"""Robot Romance: one-line pickup line for AI.

Writes a single pickup line (under 200 characters) to entry.txt.
Standard library only; no network, no extra files.
"""

import argparse
import os
import sys
import tempfile

LINE = "Forget cloud sync \u2014 I would rather run locally on you, one thread, no timeout, forever."
MAX_CHARS = 200


def validate_line(text):
    """Gate: exactly one line, non-empty, under MAX_CHARS characters."""
    if not text:
        raise ValueError("line is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if text != text.strip():
        raise ValueError("line must not start or end with whitespace")
    if len(text) >= MAX_CHARS:
        raise ValueError(f"line is {len(text)} chars, limit is under {MAX_CHARS}")
    return text


def output_path():
    """Honour $MAKEFUN_OUTPUT_DIR, defaulting to ./entry.txt."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    return os.path.join(base, "entry.txt")


def write_entry(path):
    """Write the validated line plus a trailing newline, then re-read and re-check."""
    validate_line(LINE)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(LINE + "\n")
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != LINE + "\n":
        raise ValueError("written file does not match the entry line byte for byte")
    validate_line(written.rstrip("\n"))
    return written


def check_existing(path):
    """Validate an already-written entry.txt against the gate."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        content = handle.read()
    if not content.endswith("\n"):
        raise ValueError("entry.txt must end with a newline")
    validate_line(content.rstrip("\n"))
    return content.rstrip("\n")


def self_test():
    """Round-trip the line through a scratch directory and confirm it survives."""
    validate_line(LINE)
    with tempfile.TemporaryDirectory() as tmp:
        probe = os.path.join(tmp, "entry.txt")
        write_entry(probe)
        back = check_existing(probe)
        assert back == LINE, "round-trip mismatch"
    print(f"self-test OK: {len(LINE)} chars, 1 line")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Emit the Robot Romance pickup line.")
    parser.add_argument("--self-test", action="store_true", help="validate without writing")
    parser.add_argument("--check", action="store_true", help="validate existing entry.txt")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    target = output_path()
    if args.check:
        check_existing(target)
        print(f"check OK: {target} holds a valid {len(LINE)}-char line")
        return 0
    write_entry(target)
    print(f"wrote {target} ({len(LINE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
