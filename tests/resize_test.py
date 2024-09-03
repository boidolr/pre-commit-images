import pathlib
import shutil

import pytest
from PIL import Image

from pre_commit_images.resize import main


@pytest.fixture
def images(tmpdir):
    image = "test.webp"
    path = pathlib.Path(tmpdir) / image
    test_file = pathlib.Path(__file__).parent / image
    shutil.copy(test_file, path)
    return path, test_file


def get_image_size(image):
    with Image.open(image) as im:
        return im.height, im.width


def test_resize_no_change(images):
    path, test_file = images
    height, width = get_image_size(test_file)

    assert main(("--width", f"{width}", "--height", f"{height}", str(path))) == 0

    new_height, new_width = get_image_size(path)
    assert new_height == height
    assert new_width == width
    assert test_file.stat().st_size == path.stat().st_size


def test_resize_upscale(images):
    path, test_file = images
    height, width = get_image_size(test_file)

    assert main(("--width", f"{width * 2}", "--height", f"{height * 2}", str(path))) == 0

    new_height, new_width = get_image_size(path)
    assert new_height == (height * 2)
    assert new_width == (width * 2)


def test_resize_downscale(images):
    path, test_file = images
    height, width = get_image_size(test_file)

    assert main(("--width", f"{width//2}", "--height", f"{height//2}", str(path))) == 0

    new_height, new_width = get_image_size(path)
    assert new_height == (height // 2)
    assert new_width == (width // 2)
