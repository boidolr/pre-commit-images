import sys
from pathlib import Path
from typing import Callable
from typing import Iterable


def _optimize_images(
    images: Iterable[str], optimizer_fn: Callable[[Path], Path], threshold: int
) -> bool:
    def optimize_single_image(path: str) -> None:
        fp = Path(path)
        output = optimizer_fn(fp)

        original_size = fp.stat().st_size
        diff = original_size - output.stat().st_size
        if diff > threshold:
            output.replace(fp)
            print(
                f"Optimized {path} by {diff} of {original_size} bytes ({diff/original_size:.2%})"
            )
        else:
            output.unlink()

    ret = True
    for image in images:
        try:
            optimize_single_image(image)
        except Exception as exc:
            print(
                f"Failed optimization for {image} ({exc})",
                file=sys.stderr,
            )
            ret = False

    return ret
