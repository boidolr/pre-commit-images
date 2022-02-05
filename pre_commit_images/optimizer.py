import sys
from pathlib import Path
from typing import Callable
from typing import Iterable


def _optimize_images(
    images: Iterable[str], optimizer_fn: Callable[[Path], Path], threshold: int
) -> bool:
    def bytes_to_readable(file_size: int) -> str:
        if file_size / (1024 * 1024) > 1:
            return f"{file_size / (1024 * 1024):.2f}Mb"
        elif file_size / (1024) > 1:
            return f"{(file_size/1024):.2f}Kb"
        else:
            return f"{file_size}b"

    def optimize_single_image(path: str) -> None:
        fp = Path(path)
        output = optimizer_fn(fp)

        original_size = fp.stat().st_size
        diff = original_size - output.stat().st_size
        if diff > threshold:
            output.replace(fp)
            readable_diff = bytes_to_readable(diff)
            readable_size = bytes_to_readable(original_size)
            print(
                f"Optimized {path} by {readable_diff} of {readable_size} ({diff/original_size:.2%})"
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
