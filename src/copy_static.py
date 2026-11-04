import os
import shutil

def copy_files_recursive(from_path, to_path) -> None:
    if not os.path.exists(to_path):
        os.mkdir(to_path)

    for item in os.listdir(from_path):
        from_item_path = os.path.join(from_path, item)
        to_item_path = os.path.join(to_path, item)

        print(f" * {from_item_path} -> {to_item_path}")

        if os.path.isfile(from_item_path):
            shutil.copy(from_item_path, to_item_path)
        else:
            copy_files_recursive(from_item_path, to_item_path)