import pathlib
import shutil

import pytest

from pre_commit_images.optimize_jpg import main


@pytest.fixture
def images(tmpdir):
    image = "test.jpg"
    path = pathlib.Path(tmpdir) / image
    test_file = pathlib.Path(__file__).parent / image
    shutil.copy(test_file, path)
    return path, test_file


def test_compress_jpg(images):
    path, test_file = images

    assert main(("-q", "50", str(path))) == 0
    assert test_file.stat().st_size > path.stat().st_size


def test_compress_jpg_below_threshold(images):
    path, test_file = images

    assert main(("-q", "97", "-t", "15000", str(path))) == 0
    assert test_file.stat().st_size == path.stat().st_size
