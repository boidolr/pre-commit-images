#!/usr/bin/env python3
import argparse
import sys
import warnings
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
        type=int,
        help="Deprecated: use `quality` instead.",
    )
    parser.add_argument(
        "-max",
        "--qmax",
        type=int,
        help="Deprecated: use `quality` instead.",
    )
    parser.add_argument(
        "--quality",
        default=None,
        type=int,
        help="Quality to use for AVIF images (default: 75 - from 0 up to 100)",
    )
    parser.add_argument(
        "-e",
        "--effort",
        default=4,
        type=int,
        dest="speed",
        help="Effort to use for AVIF images (default: %(default)s - range 0 down to 10)",
    )
    args = parser.parse_args(argv)

    if not args.qmin and not args.qmax and not args.quality:
        args.quality = 75

    if args.qmin and args.quality or args.qmax and args.quality:
        sys.exit("Can not use both `qmin`/`qmax` and `quality`")

    if args.qmin or args.qmax:
        warnings.warn(
            "`qmin`/`qmax` are deprecated, use `quality` instead"
            " - it will be the only option for future AVIF versions",
            category=DeprecationWarning,
        )

    options = {option: value for option, value in vars(args).items() if value}

    def optimize(source: Path, target: IO[bytes]) -> None:
        im = Image.open(source)
        im.save(target, format=im.format, **options)

    success = _optimize_images(args.filenames, optimize, args.threshold)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
