import sys
from collections.abc import Callable
from collections.abc import Iterable
from pathlib import Path
from tempfile import TemporaryFile
from typing import IO


def _optimize_images(images: Iterable[str], optimizer_fn: Callable[[Path, IO[bytes]], None], threshold: int) -> bool:
    def bytes_to_readable(file_size: int) -> str:
        if file_size / (1024 * 1024) > 1:
            return f"{file_size / (1024 * 1024):.2f}Mb"

        if file_size / (1024) > 1:
            return f"{(file_size/1024):.2f}Kb"

        return f"{file_size}b"

    def optimize_single_image(source: Path, temp: IO[bytes]) -> None:
        optimizer_fn(source, temp)

        source_size = source.stat().st_size
        diff = source_size - temp.tell()

        if diff > threshold:
            temp.seek(0)
            source.write_bytes(temp.read())

            readable_diff = bytes_to_readable(diff)
            readable_size = bytes_to_readable(source_size)
            print(f"Optimized {str(source)} by {readable_diff} of {readable_size} ({diff/source_size:.2%})")

    ret = True
    for image in images:
        try:
            with TemporaryFile() as temp:
                optimize_single_image(Path(image), temp)
        except Exception as exc:  # noqa: PERF203
            print(
                f"Failed optimization for {image} ({exc})",
                file=sys.stderr,
            )
            ret = False

    return ret
