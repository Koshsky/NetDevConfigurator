import argparse
import contextlib
import glob
import logging
import os
import subprocess
from datetime import datetime

from config import config

logger = logging.getLogger("dump")


def get_most_recent_file(directory):
    files = glob.glob(os.path.join(directory, "*"))
    if not files:
        return None
    most_recent_file = max(files, key=os.path.getmtime)

    return most_recent_file


def run_postgres_command(command, env, error_context):
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
        )
        _, error = process.communicate()

        if process.returncode != 0:
            logger.error(f"{error_context}: {error.decode()}")
            return False
        return True
    except Exception as e:
        logger.error(f"{error_context}: {e}")
        return False


def backup_postgres_db(db_params):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = f"{config['backup-folder']}/dev{timestamp}.sql"

    command = [
        "pg_dump",
        "-h",
        db_params["host"],
        "-p",
        str(db_params["port"]),
        "-U",
        db_params["username"],
        "-F",
        "c",
        "-f",
        path,
        db_params["database"],
    ]

    with contextlib.suppress(Exception):
        env = {"PGPASSWORD": db_params["password"]}
        try:
            run_postgres_command(command, env, path)
            logger.info(f"Database saved successfully to {os.path.abspath(path)}")
        except Exception as e:
            logger.error(f"{type(e)}: {e}")


def restore_postgres_db(db_params, path):
    env = {"PGPASSWORD": db_params["password"]}

    if not os.path.isfile(path):
        logger.error(f"{path} doesn't exist.")
        return

    def base_command(cmd):
        return [
            "psql",
            "-h",
            db_params["host"],
            "-p",
            str(db_params["port"]),
            "-U",
            db_params["username"],
            "-c",
            cmd,
        ]

    drop_command = base_command(f"DROP DATABASE IF EXISTS {db_params['database']};")
    create_command = base_command(f"CREATE DATABASE {db_params['database']};")
    restore_command = [
        "pg_restore",
        "-h",
        db_params["host"],
        "-p",
        str(db_params["port"]),
        "-U",
        db_params["username"],
        "-d",
        db_params["database"],
        path,
    ]

    if (
        run_postgres_command(drop_command, env, "when deleting database")
        and run_postgres_command(create_command, env, "when creating database")
        and run_postgres_command(restore_command, env, "when restoring db")
    ):
        logger.info(f"Database restored successfully from {os.path.abspath(path)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Backup or restore PostgreSQL database."
    )
    parser.add_argument("--backup", action="store_true", help="Backup the database")
    parser.add_argument("--restore", action="store_true", help="Restore the database")
    parser.add_argument(
        "-o", "--output", type=str, help="Output filename for restore operation"
    )

    args = parser.parse_args()

    if args.backup:
        backup_postgres_db(config["database"])
    elif args.restore:
        if args.output:
            path = args.output
        else:
            path = get_most_recent_file(config["backup-folder"])
        restore_postgres_db(config["database"], path)
    else:
        print("Please specify either --backup or --restore.")
