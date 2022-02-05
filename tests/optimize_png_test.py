import shutil
from pathlib import Path

from pre_commit_images.optimize_png import main


def test_compress_png(tmpdir):
    image = "test.png"
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert main((str(path),)) == 0
    assert test_file.stat().st_size > path.stat().st_size


def test_compress_png_below_threshold(tmpdir):
    image = "test.png"
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert (
        main(
            (
                "-t",
                "15000",
                str(path),
            )
        )
        == 0
    )
    assert test_file.stat().st_size == path.stat().st_size
