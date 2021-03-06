import shutil
from pathlib import Path

from pre_commit_images.optimize_webp import main


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


def test_compress_webp_below_threshold(tmpdir):
    image = "test.webp"
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert (
        main(
            (
                "-q",
                "90",
                "-t",
                "8192",
                str(path),
            )
        )
        == 0
    )
    assert test_file.stat().st_size == path.stat().st_size
