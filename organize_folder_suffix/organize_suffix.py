#! /usr/bin/env python
import os
import glob
from pathlib import Path
from collections import defaultdict
import shutil
import click


CATEGORY = {
    "papers_or_book": [".epub", '.pdf'],
    "pictures": [".jpeg", ".png"],
    "videos": [".mp4", ".mov"],
    "zipped": [".zip", ".rar"],
}


def move_folder(folder_path):
    # step_1 move to the folder
    if os.path.exists(folder_path):
        os.chdir(folder_path)
    else:
        raise OSError("The folder does not exist")


def get_all_filenames():
    # step_2 get all filenames from current working folder
    current_path = Path(os.getcwd())
    file_paths = glob.glob(str(current_path / "*"))
    filenames = [os.path.basename(file_path) for file_path in file_paths]
    return filenames


def create_folders(current_path):
    # step_3 create the folders
    for folder_name in CATEGORY.keys():
        if os.path.exists(current_path / folder_name):
            continue
        else:
            os.mkdir(current_path / folder_name)


def move_files(current_path, filenames):
    # step_4 move the files in the corresponding folder
    suffix_to_filename = defaultdict(list)
    for filename in filenames:
        file_suffix = Path(filename).suffix
        suffix_to_filename[file_suffix].append(filename)

    for folder_name in CATEGORY.keys():
        folder_path = current_path / folder_name
        folder_suffies = CATEGORY[folder_name]
        for folder_suffix in folder_suffies:
            move_file_list = suffix_to_filename[folder_suffix]
            new_file_paths = [
                folder_path / move_filename for move_filename in move_file_list
            ]
            ori_file_paths = [
                current_path / move_filename
                for move_filename in move_file_list
            ]
            for ori_path, new_path in zip(ori_file_paths, new_file_paths):
                shutil.move(str(ori_path), str(new_path))


@click.command()
@click.option('-p', '--folder_path', help='organized folder path')
def organize_folder(folder_path=None):
    if folder_path is not None:
        current_path = Path(folder_path)
    else:
        current_path = Path(os.getcwd())
    # step_1 move to the folder
    move_folder(str(current_path))
    # step_2 get all the file names
    filenames = get_all_filenames()
    # step_3 create the folders
    create_folders(current_path)
    # step_4 move the files in the corresponding folder
    move_files(current_path, filenames)


if __name__ == '__main__':
    organize_folder()
