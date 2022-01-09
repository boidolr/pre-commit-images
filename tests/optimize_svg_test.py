import shutil
from pathlib import Path

from hooks.optimize_svg import main


def test_compress_svg(tmpdir):
    image = "test.svg"
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert main((str(path),)) == 0
    assert test_file.stat().st_size > path.stat().st_size
