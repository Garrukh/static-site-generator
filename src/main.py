import os
import shutil
import sys

from copy_static import copy_files_recursive
from page_generation import generate_pages_recursive

from_path = "./static"
to_path = "./docs"

content_path = "./content"
template_path = "./template.html"

def main() -> None:
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    print("Deleting destination directory...")
    if os.path.exists(to_path):
        shutil.rmtree(to_path)

    print("Copying from target to destination...")
    copy_files_recursive(from_path, to_path)

    print("Generating pages...")
    generate_pages_recursive(content_path, template_path, to_path, basepath)

if __name__ == "__main__":
    main()