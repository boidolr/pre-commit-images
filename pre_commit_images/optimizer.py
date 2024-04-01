import sys
from collections.abc import Callable
from collections.abc import Iterable
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import IO


def _bytes_to_readable(file_size: int) -> str:
    if file_size / (1024 * 1024) > 1:
        return f"{file_size / (1024 * 1024):.2f}Mb"

    if file_size / (1024) > 1:
        return f"{(file_size/1024):.2f}Kb"

    return f"{file_size}b"


def _optimize_images(images: Iterable[str], optimizer: Callable[[Path, IO[bytes]], None], threshold: int) -> bool:
    def keep_smaller_image(source: Path, candidate: IO[bytes]) -> None:
        source_size = source.stat().st_size
        diff = source_size - candidate.tell()

        if diff > threshold:
            candidate.seek(0)
            source.write_bytes(candidate.read())

            readable_diff = _bytes_to_readable(diff)
            readable_size = _bytes_to_readable(source_size)
            print(f"Optimized {source} by {readable_diff} of {readable_size} ({diff/source_size:.2%})")

    ret = True
    for image in images:
        try:
            with SpooledTemporaryFile() as temp:
                image_path = Path(image)
                optimizer(image_path, temp)
                keep_smaller_image(image_path, temp)
        except Exception as exc:  # noqa: PERF203
            print(
                f"Failed optimization for {image} ({exc})",
                file=sys.stderr,
            )
            ret = False

    return ret
