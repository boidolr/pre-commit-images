#!/usr/bin/env python3
import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import IO

from scour import scour

from .optimizer import _optimize_images


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to optimize.")
    parser.add_argument(
        "-t",
        "--threshold",
        default=1024,
        type=int,
        help="Minimum improvement to replace file in bytes (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    def optimize(source: Path, target: IO[bytes]) -> None:
        data = source.read_text(encoding="utf-8")
        options = {
            "enable_viewboxing": True,
            "strip_ids": True,
            "strip_comments": True,
            "shorten_ids": True,
            "indent_type": "none",
        }
        output = scour.scourString(data, options)

        target.write(output.encode("utf-8"))

    success = _optimize_images(args.filenames, optimize, args.threshold)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
