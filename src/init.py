import os
import shutil

def init_directory(path_to_make_list):
    # path_to_make_list = ['./load', './material', './geom', './model']
    for path_to_make in path_to_make_list:
        if os.path.exists(path_to_make):
            shutil.rmtree(path_to_make)
        os.mkdir(path_to_make)