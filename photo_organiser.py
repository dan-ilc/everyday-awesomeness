"""Photo organiser.

To use this script, please do the following:
1. Connect your phone to the target computer
2. Connect your backup drive
3. Hit run!

It will do the following:
1. MOVE PHOTOS For each photo in the target dir on the phone:
- locate the correct dir on the pc harddrive
- copy it there if it already exists

2. BACKUP - it will do an rsync-like operation to sync up the hdd with the photo
drive on the computer.
"""

import argparse
import filecmp
import os
import shutil
import subprocess
from datetime import datetime


def enable_write_permmissions(dir: str):
    # Numeric mode value for read-write permissions for the owner
    mode = 0o700  # This grants read, write, and execute permissions to the owner
    try:
        os.chmod(dir, mode)
        print(f"Permissions of folder '{dir}' updated successfully.")
    except OSError as e:
        print(f"Error: Failed to update permissions of folder '{dir}': {e}")


def get_timestamp_from_filename(filename: str) -> datetime:
    try:
        timestamp_str = os.path.splitext(filename)[0].split('_')[1]
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d')
        return timestamp
    except (IndexError, ValueError):
        return None


def organize_photos(input_dir: str, output_dir: str) -> None:
    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            timestamp = get_timestamp_from_filename(file)
            if not timestamp:
                # print("using actual file timestamp")
                creation_time = os.path.getctime(file_path)
                timestamp = datetime.fromtimestamp(creation_time)
            year_folder_name = timestamp.strftime("%Y")
            # print(year_folder_name)
            month_folder_name = timestamp.strftime('%m-%b')
            output_subdir = os.path.join(output_dir, year_folder_name,
                                         month_folder_name)
            # print(f"{file_path} --> {output_subdir}")
            os.makedirs(output_subdir, exist_ok=True)
            dst_path = os.path.join(output_subdir, file)
            if not os.path.exists(dst_path):
                print(dst_path)
                shutil.copy2(file_path, output_subdir)


def is_subdirectory(child_dir: str, parent_dir: str) -> bool:
    parent_dir = os.path.abspath(parent_dir)
    child_dir = os.path.abspath(child_dir)
    return child_dir.startswith(parent_dir)


def sync_folders(source: str, dest: str):
    """Sync all the files from source (master) to dest (slave)
    """
    subprocess.run(["rsync", "-av", source + "/", dest])


def directories_are_the_same(dir1: str, dir2: str):
    dir_cmp = filecmp.dircmp(dir1, dir2)

    if dir_cmp.left_only or dir_cmp.right_only or dir_cmp.diff_files:
        return False

    for common_file in dir_cmp.common_files:
        file1 = os.path.join(dir1, common_file)
        file2 = os.path.join(dir2, common_file)

        if os.path.getsize(file1) != os.path.getsize(file2):
            return False

    for common_dir in dir_cmp.common_dirs:
        subdir1 = os.path.join(dir1, common_dir)
        subdir2 = os.path.join(dir2, common_dir)

        if not directories_are_the_same(subdir1, subdir2):
            return False

    return True


def main():
    parser = argparse.ArgumentParser(description='Organize photos by month.')
    parser.add_argument('--phone',
                        required=True,
                        help='Path to the input directory.')
    parser.add_argument('--pc',
                        required=True,
                        help='Path to the output directory.')
    parser.add_argument('--hdd', help='[Optional] path to backup directory.')
    args = parser.parse_args()

    phone_dir = args.phone
    pc_dir = args.pc
    hdd_dir = args.hdd
    # Note - need to run chmod -R +w on the output_dir.

    if not os.path.isdir(phone_dir):
        print('Error: Input directory does not exist.')
        return

    if is_subdirectory(phone_dir, pc_dir):
        raise RuntimeError(
            'Error: Output directory cannot be inside the input directory.')

    os.makedirs(pc_dir, exist_ok=True)
    enable_write_permmissions(pc_dir)
    organize_photos(phone_dir, pc_dir)
    print('Photos organized successfully.')

    # now sync them
    if hdd_dir is not None:
        print("Hdd")
        os.makedirs(hdd_dir, exist_ok=True)
        print(hdd_dir)
        sync_folders(pc_dir, hdd_dir)
        assert directories_are_the_same(pc_dir, hdd_dir)


if __name__ == '__main__':
    main()
