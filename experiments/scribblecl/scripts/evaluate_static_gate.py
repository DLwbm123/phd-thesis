#!/usr/bin/env python3
"""Compare two project-owned static checkpoints using the foreground gate."""

import argparse
import json
from pathlib import Path

from scribblecl.gate import compare_validations, load_checkpoint_validation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("previous")
    parser.add_argument("current")
    parser.add_argument("output")
    parser.add_argument("label")
    args = parser.parse_args()
    result = compare_validations(
        load_checkpoint_validation(args.previous),
        load_checkpoint_validation(args.current),
        args.label,
    )
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["decision"] == "PASS" else 2)


if __name__ == "__main__":
    main()
