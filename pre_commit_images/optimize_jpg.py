#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Optional
from typing import Sequence

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
        "-q",
        "--quality",
        default=80,
        type=int,
        help="Quality to use for JPG images (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    def optimize(path: Path) -> Path:
        bkp = path.with_suffix(path.suffix + ".bkp")
        im = Image.open(path)
        im.save(bkp, format=im.format, optimize=True, progressive=True, quality=args.quality)
        return bkp

    success = _optimize_images(args.filenames, optimize, args.threshold)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
