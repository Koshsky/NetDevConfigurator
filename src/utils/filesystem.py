import os
import fnmatch


def find_most_recent_file(directory: str, pattern: str) -> str:
    most_recent_file = None
    most_recent_time = 0

    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename, pattern):
            file_path = os.path.join(directory, filename)
            file_mtime = os.path.getmtime(file_path)
            if file_mtime > most_recent_time:
                most_recent_time = file_mtime
                most_recent_file = filename

    return most_recent_file
