#!/usr/bin/env python3
import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import IO
from typing import Optional

import pillow_avif  # noqa: F401
from PIL import Image

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

    def optimize(source: Path, target: IO[bytes]) -> None:
        im = Image.open(source)
        im.save(target, format=im.format, speed=args.effort, qmin=args.qmin, qmax=args.qmax)

    success = _optimize_images(args.filenames, optimize, args.threshold)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
