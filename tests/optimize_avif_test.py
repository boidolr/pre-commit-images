import pathlib
import shutil

import pytest

from pre_commit_images.optimize_avif import main


@pytest.fixture
def images(tmpdir):
    test_file = pathlib.Path(__file__).parent / "test.avif"
    path = pathlib.Path(tmpdir) / "test.avif"
    shutil.copy(test_file, path)
    return path, test_file


def test_compress_avif(images):
    path, test_file = images
    assert main(("--quality", "75", "-e", "0", str(path))) == 0
    assert test_file.stat().st_size > path.stat().st_size


def test_compress_avif_below_threshold(images):
    path, test_file = images
    assert (
        main(
            (
                "--quality",
                "90",
                "-e",
                "10",
                "-t",
                "6144",
                str(path),
            )
        )
        == 0
    )
    assert test_file.stat().st_size == path.stat().st_size
