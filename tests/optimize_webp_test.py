import shutil
from pathlib import Path

from hooks.optimize_webp import main


def test_compress_webp(tmpdir):
    image = "test.webp"
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert (
        main(
            (
                "-q",
                "10",
                str(path),
            )
        )
        == 0
    )
    assert test_file.stat().st_size > path.stat().st_size
