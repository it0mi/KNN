import sys
from urllib.request import urlretrieve
import pathlib
import zipfile
import glob
from shutil import copy2, rmtree


if __name__ == "__main__":
    cwd = pathlib.Path.cwd()
    temp_path = cwd / "tmp"
    pathlib.Path(temp_path).mkdir(parents=True, exist_ok=True)

    if not pathlib.Path(temp_path / "faces-20150624.zip").exists():
        path, headers = urlretrieve("https://figshare.com/ndownloader/files/2134461", "tmp/faces-20150624.zip")

    if not pathlib.Path(temp_path / "data").exists():
        with zipfile.ZipFile(temp_path / "faces-20150624.zip", 'r') as zip_ref:
            zip_ref.extractall(temp_path / "data")

    face_dir = temp_path / "data" / "faces"
    classed_faces_dir = cwd / "data"
    pathlib.Path(classed_faces_dir).mkdir(parents=True, exist_ok=True)
    for filename in glob.glob(f"{face_dir}/*.jpg"):
        if not (classed_faces_dir / pathlib.Path(filename).parts[-1]).exists():
            copy2(filename, classed_faces_dir)

    if "-c" in sys.argv or "--clean" in sys.argv:
        rmtree(temp_path)
