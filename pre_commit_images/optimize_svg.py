#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Optional
from typing import Sequence

from scour import scour

from .optimizer import _optimize_images


def main(argv: Optional[Sequence[str]] = None) -> int:
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

    def optimize(path: Path) -> Path:
        data = path.read_text(encoding="utf-8")
        options = {
            "enable_viewboxing": True,
            "strip_ids": True,
            "strip_comments": True,
            "shorten_ids": True,
            "indent_type": "none",
        }
        output = scour.scourString(data, options)

        bkp = path.with_suffix(path.suffix + ".bkp")
        bkp.write_text(output, encoding="utf-8")
        return bkp

    success = _optimize_images(args.filenames, optimize, args.threshold)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
