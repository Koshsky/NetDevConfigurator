import os
import glob

from config import config


def get_most_recent_file(directory):
    files = glob.glob(os.path.join(directory, "*"))
    if not files:
        return None
    most_recent_file = max(files, key=os.path.getmtime)

    return most_recent_file


most_recent_file = get_most_recent_file(config["backup-folder"])

if most_recent_file:
    print(f"Самый свежий файл: {most_recent_file}")
else:
    print("В директории нет файлов.")
