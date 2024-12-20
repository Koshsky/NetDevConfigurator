import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from internal.database.services import *

connection_string = "postgresql://postgres:postgres@localhost:5432/device_registry"
try:
    engine = create_engine(connection_string)
    connect = engine.connect()  # Checking the connection
    connect.close()

    session = sessionmaker(bind=engine)()
    entity_services = setup_database_services(session)
    print("Connection successful.")
except Exception as error:
    print(f'Error: {str(error)}')

try:
    with open('data.json', 'r') as file:
        templates = json.load(file)
    family_id = entity_services['family'].get_by_name(input('enter family name: ').strip().capitalize()).id
except Exception as error:
    print(f'Error: {str(error)}')

for template in templates:
    template['family_id'] = family_id
    entity_services['template'].create(template)
