import pathlib
import shutil

import pytest

from pre_commit_images.optimize_webp import main


@pytest.fixture
def images(tmpdir):
    image = "test.webp"
    path = pathlib.Path(tmpdir) / image
    test_file = pathlib.Path(__file__).parent / image
    shutil.copy(test_file, path)
    return path, test_file


def test_compress_webp(images):
    path, test_file = images

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


def test_compress_webp_below_threshold(images):
    path, test_file = images

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
