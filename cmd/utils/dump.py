import subprocess
import os
import argparse
from datetime import datetime

db_params = ['localhost', "5432", "device_registry", 'postgres', 'postgres']

def backup_postgres_db(db_params):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    path = f"./.backups/dev{timestamp}.sql"
    host, port, database_name, user, password = db_params
    
    command = [
        'pg_dump',
        '-h', host,
        '-p', port,
        '-U', user,
        '-F', 'c',
        '-f', path,
        database_name
    ]

    env = {'PGPASSWORD': password}

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        output, error = process.communicate()

        if process.returncode != 0:
            print(f'Error creating dump: {error.decode()}')
        else:
            print(f'Database dump successfully created: {path}')

    except Exception as e:
        print(f'Error: {e}')


def restore_postgres_db(db_params, path):
    host, port, database_name, user, password = db_params

    if not os.path.isfile(path):
        print(f'Error: {path} doesn\'t exist.')
        return

    drop_command = [
        'psql',
        '-h', host,
        '-p', port,
        '-U', user,
        '-c', f'DROP DATABASE IF EXISTS {database_name};'
    ]

    create_command = [
        'psql',
        '-h', host,
        '-p', port,
        '-U', user,
        '-c', f'CREATE DATABASE {database_name};'
    ]

    env = {'PGPASSWORD': password}

    try:
        drop_process = subprocess.Popen(drop_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        _, drop_error = drop_process.communicate()

        if drop_process.returncode != 0:
            print(f'Error when deleting database: {drop_error.decode()}')
            return
        
        print(f'Database {database_name} successfully deleted.')

        create_process = subprocess.Popen(create_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        create_output, create_error = create_process.communicate()

        if create_process.returncode != 0:
            print(f'Error when creating database: {create_error.decode()}')
            return
        
        print(f'Database {database_name} successfully created')

        restore_command = [
            'pg_restore',
            '-h', host,
            '-p', port,
            '-U', user,
            '-d', database_name,
            path
        ]

        restore_process = subprocess.Popen(restore_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        restore_output, restore_error = restore_process.communicate()

        if restore_process.returncode != 0:
            print(f': {restore_error.decode()}')
        else:
            print('Database restored successfully')

    except Exception as e:
        print(f'Error: {e}')

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
