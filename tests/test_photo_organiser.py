"""Test photo organiser.

This script will:
1. Create 3 temp file groups:
a. Phone (with a list of photos)
b. HDD (with some files, but organised)
c. Ext HDD (with some other organised files)
"""


import os
import shutil
import unittest
import tempfile
# Import the sync_folders function from the previous code
# from photo_organiser import sync_folders


def print_tree(dir_path: str, padding=""):
    """Produces something like
    config-files-v127
    |-- mcc-driven
    |   |-- config
    |   |   |-- annotator_label_sets
    |   |   |   |-- on_road_label_set.json
    |   |   |   |-- carp_rat2_label_set.json

    Could probably be improved with Path.rglob()
    """
    files = os.listdir(dir_path)
    if not padding:
        print(os.path.basename(dir_path))
    for file in files:
        full_path = os.path.join(dir_path, file)
        print(padding + "|-- " + file)
        # If the current item is a folder, repeat for its contents
        if os.path.isdir(full_path):
            print_tree(full_path, padding + "|   ")


class SyncFoldersTest(unittest.TestCase):
    def setUp(self):
        phone_dir_tmp = tempfile.TemporaryDirectory(dir="/tmp",suffix="-phone")
        phone_dir = phone_dir_tmp.name

        os.makedirs(os.path.join(phone_dir, "photos1"))
        os.makedirs(os.path.join(phone_dir, "photos2"))
        with open(os.path.join(phone_dir, "photos1", "file1.jpg"), "w") as f:
            f.write("Sample content 2")
        with open(os.path.join(phone_dir, "photos1", "file2.png"), "w") as f:
            f.write("Sample content 2")
        with open(os.path.join(phone_dir, "photos1", "file3.jpg"), "w") as f:
            f.write("Sample content 2")
        subfolder_path = os.path.join(phone_dir, "photos1", "subfolder")
        os.makedirs(subfolder_path)
        with open(os.path.join(subfolder_path, "file3.txt"), "w") as f:
            f.write("Sample content 3")
        print()
        print_tree(phone_dir)
        import time
        time.sleep(10303)
        computer_dir_tmp = tempfile.TemporaryDirectory(suffix="-phone")


    def test_sync_folders(self):
        print("Hi")

    def tearDown(self):
        # Clean up the temporary folder structure
        shutil.rmtree(self.source_folder)
        shutil.rmtree(self.destination_folder)

if __name__ == '__main__':
    unittest.main()
