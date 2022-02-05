import shutil
from pathlib import Path

from pre_commit_images.optimize_avif import main


def test_compress_avif(tmpdir):
    image = "test.avif"
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert main(("-min", "63", "-max", "63", "-e", "0", str(path))) == 0
    assert test_file.stat().st_size > path.stat().st_size


def test_compress_avif_below_threshold(tmpdir):
    image = "test.avif"
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert (
        main(
            (
                "-min",
                "10",
                "-max",
                "20",
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
