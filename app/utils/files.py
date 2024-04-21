import os
import shutil


def remove_tmp_files():
    for file_obj in os.scandir('/tmp'):
        check_str = file_obj.name[:3]
        if 'tmp' not in check_str and 'snap' not in check_str:
            continue
        if file_obj.is_dir():
            shutil.rmtree(file_obj.path)
        else:
            os.remove(file_obj.path)
