import pathlib
import shutil

import pytest

from pre_commit_images.optimize_svg import main


@pytest.fixture
def images(tmpdir):
    image = "test.svg"
    path = pathlib.Path(tmpdir) / image
    test_file = pathlib.Path(__file__).parent / image
    shutil.copy(test_file, path)
    return path, test_file


def test_compress_svg(images):
    path, test_file = images

    assert main((str(path),)) == 0
    assert test_file.stat().st_size > path.stat().st_size


def test_compress_svg_below_threshold(images):
    path, test_file = images

    assert main(("-t", "4096", str(path))) == 0
    assert test_file.stat().st_size == path.stat().st_size
