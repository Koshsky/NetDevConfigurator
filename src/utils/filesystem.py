import fnmatch
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def find_most_recent_file(directory: str, pattern: str) -> Optional[str]:
    """
    Finds the most recent file in a directory matching a given pattern.

    Args:
        directory: The directory to search in.
        pattern: The file pattern to match (e.g., "*.txt").

    Returns:
        The name of the most recent file, or None if no matching files are found.
        Raises FileNotFoundError if the directory does not exist.
    """
    logger.debug(
        "Starting search for most recent file in '%s' matching '%s'", directory, pattern
    )

    dir_path = Path(directory)
    if not dir_path.exists():
        logger.error("Directory not found: %s", directory)
        raise FileNotFoundError(f"Directory not found: {directory}")

    most_recent_file = None
    most_recent_time = 0

    for file_path in dir_path.iterdir():
        if file_path.is_file() and fnmatch.fnmatch(file_path.name, pattern):
            file_mtime = file_path.stat().st_mtime
            logger.debug(
                "File '%s' matches pattern, mtime: %s", file_path.name, file_mtime
            )
            if file_mtime > most_recent_time:
                logger.debug(
                    "File '%s' is newer than current most recent file",
                    file_path.name,
                )
                most_recent_time = file_mtime
                most_recent_file = file_path.name

    if most_recent_file is None:
        logger.warning(
            "No files found matching pattern '%s' in directory '%s'", pattern, directory
        )
    else:
        logger.debug("Most recent file found: %s", most_recent_file)

    return most_recent_file
