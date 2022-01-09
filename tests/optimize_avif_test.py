import shutil
from pathlib import Path

from hooks.optimize_avif import main


def test_compress_avif(tmpdir):
    image = "test.avif"
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert main(("-min", "63", "-max", "63", "-e", "0", str(path))) == 0
    assert test_file.stat().st_size > path.stat().st_size
