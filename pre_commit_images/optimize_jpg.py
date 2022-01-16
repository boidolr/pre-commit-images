#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Optional
from typing import Sequence

from PIL import Image


def _pillow(path: Path, quality: int) -> Path:
    bkp = path.with_suffix(path.suffix + ".bkp")
    im = Image.open(path)
    im.save(bkp, format=im.format, optimize=True, progressive=True, quality=quality)
    return bkp


def optimize_jpg(path: str, threshold: int, quality: int) -> None:
    fp = Path(path)

    output = _pillow(fp, quality)

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
    parser.add_argument(
        "-q",
        "--quality",
        default=80,
        type=int,
        help="Quality to use for JPG images (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    ret = 0
    for file in args.filenames:
        try:
            optimize_jpg(file, args.threshold, args.quality)
        except Exception as exc:
            print(
                f"Failed optimization for {file} ({exc})",
                file=sys.stderr,
            )
            ret = 1

    return ret


if __name__ == "__main__":
    sys.exit(main())
