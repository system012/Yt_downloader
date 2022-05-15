import os
import time
from constants import downloaded_dir

def remove_old_files():
    files = os.listdir(downloaded_dir)
    for file in files:
        file_loc = os.path.join(downloaded_dir, file)
        file_stat = os.stat(file_loc)
        file_age = (time.time()-file_stat.st_mtime)
        if file_age > 86400:
            os.remove(file_loc)
            print(f'File named {file} removed')