import os
import shutil
from site_generator import *

def copy_static_contents(dir1 : str, dir2 : str) -> None:

    if not os.path.exists(dir1):
        raise Exception("Static contents directory not found")

    if os.path.exists(dir2):
        print(f"Erasing old contents from '{dir2}' directory")
        shutil.rmtree(dir2)

    print(f"Creating new '{dir2}' directory")
    os.mkdir(dir2)

    if os.path.exists(dir1):

        dir1_contents = os.listdir(dir1)

        for elem in dir1_contents:
            if os.path.isfile(f"{dir1}/{elem}"):
                print(f"Copying of '{dir1}/{elem}' to '{dir2}/{elem}'")
                shutil.copy(f"{dir1}/{elem}", f"{dir2}/{elem}")
            else:
                print(f"Creating directory '{dir2}/{elem}'")
                os.mkdir(f"{dir2}/{elem}")
                print(f"Transferring files from '{dir1}/{elem}' to '{dir2}/{elem}'")
                copy_static_contents(f"{dir1}/{elem}", f"{dir2}/{elem}")
    else:
        shutil.copy(f"{dir1}", f"{dir2}")


def main():
    copy_static_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    
if __name__ == "__main__":
    main()