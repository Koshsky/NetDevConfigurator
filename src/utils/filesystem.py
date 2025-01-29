import fnmatch
import os


def find_most_recent_file(directory: str, pattern: str) -> str:
    most_recent_file = None
    most_recent_time = float("inf")

    for filename in os.listdir(directory):
        filename.strip()
        if fnmatch.fnmatch(filename, pattern):
            file_path = os.path.join(directory, filename)
            file_mtime = os.path.getmtime(file_path)
            if file_mtime < most_recent_time:
                most_recent_time = file_mtime
                most_recent_file = filename
    if most_recent_file is None:
        raise FileNotFoundError(
            f"No files found matching the pattern {pattern} in the directory {directory}"
        )
    return most_recent_file
