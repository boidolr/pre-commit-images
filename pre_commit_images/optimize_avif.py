#!/usr/bin/env python3
import argparse
import sys
import warnings
from collections.abc import Sequence
from pathlib import Path
from typing import IO

from PIL import Image

from .optimizer import _optimize_images

try:
    import pillow_avif  # noqa: F401
except ImportError:
    warnings.warn('Missing `pillow_avif` dependency, install optional "[avif]" dependency group')
    sys.exit(1)


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
    parser.add_argument(
        "--quality",
        default=75,
        type=int,
        help="Quality to use for AVIF images (default: 75 - from 0 up to 100)",
    )
    parser.add_argument(
        "-e",
        "--effort",
        default=4,
        type=int,
        metavar="EFFORT",
        dest="speed",
        help="Effort to use for AVIF images (default: %(default)s - range 0 down to 10)",
    )
    args = parser.parse_args(argv)

    def optimize(source: Path, target: IO[bytes]) -> None:
        im = Image.open(source)
        im.save(target, format=im.format, speed=args.speed, quality=args.quality)

    success = _optimize_images(args.filenames, optimize, args.threshold)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
