#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Optional
from typing import Sequence

from scour import scour


def _optimize_scour(path: Path) -> Path:
    data = path.read_text()
    options = {
        "enable_viewboxing": True,
        "strip_ids": True,
        "strip_comments": True,
        "shorten_ids": True,
        "indent_type": "none",
    }
    output = scour.scourString(data, options)

    bkp = path.with_suffix(path.suffix + ".bkp")
    bkp.write_text(output)
    return bkp


def optimize_svg(path: str, threshold: int) -> None:
    fp = Path(path)
    output = _optimize_scour(fp)

    original_size = fp.stat().st_size
    diff = original_size - output.stat().st_size
    if diff > threshold:
        output.replace(fp)
        print(
            f"Optimized {path} by {diff} of {original_size} bytes ({diff/original_size:.2%})"
        )
    else:
        output.unlink()


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

    ret = 0
    for file in args.filenames:
        try:
            optimize_svg(file, args.threshold)
        except Exception as exc:
            print(
                f"Failed optimization for {file} ({exc})",
                file=sys.stderr,
            )
            ret = 1

    return ret


if __name__ == "__main__":
    sys.exit(main())
