#!/usr/bin/env python3
import argparse
import fractions
import sys
import warnings
from collections.abc import Iterable
from collections.abc import Sequence
from pathlib import Path

from PIL import Image

try:
    import pillow_avif  # noqa: F401
except ImportError:
    warnings.warn('Missing `pillow_avif` dependency, install optional "[avif]" dependency group')
    sys.exit(1)


def _resize_images(images: Iterable[str], width: int, height: int) -> bool:
    def resize_image(source: Path) -> None:
        with Image.open(source) as im:
            if im.height == height and im.width == width:
                return

            im.resize((width, height), resample=Image.Resampling.LANCZOS, reducing_gap=3.0).save(
                source, format=im.format, optimize=True
            )

            source_factor = fractions.Fraction(im.width, im.height).limit_denominator(50)
            target_factor = fractions.Fraction(width, height).limit_denominator(50)
            format_change = (
                " from aspect {source_factor} to {target_factor} (!)" if source_factor != target_factor else ""
            )
            print(f"Resized {source} to {width}/{height}{format_change}")

    ret = True
    for image in images:
        try:
            resize_image(Path(image))
        except Exception as exc:  # noqa: PERF203
            print(
                f"Failed to resize {image} ({exc})",
                file=sys.stderr,
            )
            ret = False

    return ret


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to resize.")
    parser.add_argument("--width", type=int, help="Specify width for resized image")
    parser.add_argument("--height", type=int, help="Specify height for resized image")
    args = parser.parse_args(argv)

    success = _resize_images(args.filenames, args.width, args.height)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
