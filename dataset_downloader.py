import sys
from urllib.request import urlretrieve
import pathlib
import zipfile
import glob
from shutil import copy2, rmtree
import subprocess


def download_dataset(clean=False):
    temp_path = cwd / "tmp"
    pathlib.Path(temp_path).mkdir(parents=True, exist_ok=True)

    if not pathlib.Path(temp_path / "faces-20150624.zip").exists():
        _, _ = urlretrieve("https://figshare.com/ndownloader/files/2134461", "tmp/faces-20150624.zip")

    if not pathlib.Path(temp_path / "data").exists():
        with zipfile.ZipFile(temp_path / "faces-20150624.zip", 'r') as zip_ref:
            zip_ref.extractall(temp_path / "data")

    face_dir = temp_path / "data" / "faces"
    classed_faces_dir = cwd / "data"
    pathlib.Path(classed_faces_dir).mkdir(parents=True, exist_ok=True)
    counter = 0
    for filename in glob.glob(f"{face_dir}/*.jpg"):
        counter += 1
        pathlib.Path(classed_faces_dir / str(counter)).mkdir(parents=True, exist_ok=True)
        new_path = pathlib.Path(classed_faces_dir / str(counter) / pathlib.Path(filename).parts[-1])

        if not new_path.exists():
            copy2(filename, new_path)

    if clean:
        rmtree(temp_path)


def apply_styles(folder):
    return


if __name__ == "__main__":
    cwd = pathlib.Path.cwd()
    download_flag = False
    clean_flag = False
    style_flag = False
    style_folder = ""

    if "-c" in sys.argv or "--clean" in sys.argv:
        clean_flag = True
    if len(sys.argv) > 1 and ("-d" in sys.argv or "--download" in sys.argv):
        download_flag = True
    if len(sys.argv) > 2 and ("-s" in sys.argv or "--style" in sys.argv):
        if "-s" in sys.argv:
            idx = sys.argv.index("-s")
        else:
            idx = sys.argv.index("--style")
        style_flag = True
        if pathlib.Path(cwd / sys.argv[idx+1]).exists():
            style_folder = pathlib.Path(cwd / sys.argv[idx+1])
        else:
            print("Style folder not found.", file=sys.stderr)
            exit(-1)

    if not download_flag and not style_flag:
        download_flag = True

    if download_flag:
        download_dataset(clean_flag)

    if style_flag:
        apply_styles(style_folder)

