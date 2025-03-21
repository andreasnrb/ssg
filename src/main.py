import os
import shutil
import sys

from copystatic import copy_files_recursive
from helpers import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
dir_path_templates = "./templates"


def main():
    # Check if at least one command line argument is provided
    if len(sys.argv) <= 1:
        print("Error: Missing basepath argument")
        print('Usage: python3 main.py "/REPO_NAME/"')
        sys.exit(1)  # Exit with a non-zero status to indicate error

    # If we get here, we have at least one argument
    basepath = sys.argv[1]
    print(f"Using basepath: {basepath}")

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(
        dir_path_content, dir_path_templates, dir_path_public, basepath
    )


main()
