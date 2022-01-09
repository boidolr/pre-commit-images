#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Optional
from typing import Sequence

import pillow_avif  # noqa: F401
from PIL import Image


def _pillow(path: Path, qmin: int, qmax: int, effort: int) -> Path:
    bkp = path.with_suffix(path.suffix + ".bkp")
    im = Image.open(path)
    im.save(bkp, format=im.format, speed=effort, qmin=qmin, qmax=qmax)
    return bkp


def optimize_avif(path: str, threshold: int, qmin: int, qmax: int, effort: int) -> None:
    fp = Path(path)

    output = _pillow(fp, qmin, qmax, effort)

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
        "-min",
        "--qmin",
        default=50,
        type=int,
        help="Minimum quality to use for AVIF images (default: %(default)s - from 0 down to 63)",
    )
    parser.add_argument(
        "-max",
        "--qmax",
        default=30,
        type=int,
        help="Quality to use for AVIF images (default: %(default)s - from 0 down to 63)",
    )
    parser.add_argument(
        "-e",
        "--effort",
        default=4,
        type=int,
        help="Effort to use for AVIF images (default: %(default)s - range 0 down to 10)",
    )
    args = parser.parse_args(argv)

    ret = 0
    for file in args.filenames:
        try:
            optimize_avif(file, args.threshold, args.qmin, args.qmax, args.effort)
        except Exception as exc:
            print(
                f"Failed optimization for {file} ({exc})",
                file=sys.stderr,
            )
            ret = 1

    return ret


if __name__ == "__main__":
    sys.exit(main())
