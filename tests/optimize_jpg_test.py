import shutil
from pathlib import Path

from hooks.optimize_jpg import main


def test_compress_jpg(tmpdir):
    image = "test.jpg"
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert main(("-q", "50", str(path))) == 0
    assert test_file.stat().st_size > path.stat().st_size
