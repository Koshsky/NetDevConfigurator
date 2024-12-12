import subprocess
import contextlib
import os
import argparse
from datetime import datetime

db_params = ['localhost', "5432", "device_registry", 'postgres', 'postgres']

def run_postgres_command(command, env, error_context):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        _, error = process.communicate()
        
        if process.returncode != 0:
            print(f'Error {error_context}: {error.decode()}')
            return False
        return True
    except Exception as e:
        print(f'Error {error_context}: {e}')
        return False
    

def backup_postgres_db(db_params):
    host, port, database_name, user, password = db_params
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = f"./.backups/dev{timestamp}.sql"

    command = [
        'pg_dump',
        '-h', host,
        '-p', port,
        '-U', user,
        '-F', 'c',
        '-f', path,
        database_name
    ]

    with contextlib.suppress(Exception):
        env = {'PGPASSWORD': password}
        run_postgres_command(command, env, path)

def restore_postgres_db(db_params, path):
    host, port, database_name, user, password = db_params
    env = {'PGPASSWORD': password}

    if not os.path.isfile(path):
        print(f'Error: {path} doesn\'t exist.')
        return

    base_command = lambda cmd: [
        'psql', '-h', host, '-p', port, '-U', user, '-c', cmd
    ]

    drop_command = base_command(f'DROP DATABASE IF EXISTS {database_name};')
    create_command = base_command(f'CREATE DATABASE {database_name};')
    restore_command = [
        'pg_restore', '-h', host, '-p', port, '-U', user, '-d', database_name, path
    ]

    if (run_postgres_command(drop_command, env, 'when deleting database') and
        run_postgres_command(create_command, env, 'when creating database') and
        run_postgres_command(restore_command, env, 'when restoring db')):
        print('Database restored successfully')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup or restore PostgreSQL database.')
    parser.add_argument('--backup', action='store_true', help='Backup the database')
    parser.add_argument('--restore', action='store_true', help='Restore the database')
    parser.add_argument('-o', '--output', type=str, help='Output filename for restore operation')

    args = parser.parse_args()

    if args.backup:
        backup_postgres_db(db_params)
    elif args.restore:
        if args.output:
            restore_postgres_db(db_params, args.output)
        else:
            print("Output filename must be specified for restore operation using -o or --output.")
    else:
        print("Please specify either --backup or --restore.")
