import shutil
from pathlib import Path

import pytest

from pre_commit_images.optimize_avif import main


@pytest.fixture
def original_image(tmpdir):
    return Path(__file__).parent / "test.avif"


@pytest.fixture
def image(tmpdir, original_image):
    path = Path(tmpdir) / "test.avif"
    shutil.copy(original_image, path)
    return path


def test_qmin_qmax_deprecated(image):
    with pytest.deprecated_call():
        assert main(("-min", "0", str(image))) == 0


def test_qmin_qmax_and_quality(image):
    with pytest.raises(SystemExit) as wrapped_exit:
        assert main(("-min", "10", "--quality", "20", str(image))) == 1
        assert wrapped_exit.type == SystemExit
        assert wrapped_exit.value.code == 1


def test_compress_avif(original_image, image):
    assert main(("--quality", "75", "-e", "0", str(image))) == 0
    assert original_image.stat().st_size > image.stat().st_size


def test_compress_avif_below_threshold(original_image, image):
    assert (
        main(
            (
                "--quality",
                "90",
                "-e",
                "10",
                "-t",
                "6144",
                str(image),
            )
        )
        == 0
    )
    assert original_image.stat().st_size == image.stat().st_size
