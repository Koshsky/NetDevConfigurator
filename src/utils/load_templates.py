from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.services import setup_database_services

connection_string = "postgresql://postgres:postgres@localhost:5432/device_registry"
templates = [{}, {}]
try:
    engine = create_engine(connection_string)
    connect = engine.connect()  # Checking the connection
    connect.close()

    session = sessionmaker(bind=engine)()
    entity_services = setup_database_services(session)
    print("Connection successful.")
except Exception as error:
    print(f"Error: {str(error)}")


try:
    family_id = (
        entity_services["family"].get_by_name(("MES14xx/24xx/34xx/37xx").strip()).id
    )

    for template in templates:
        template["family_id"] = family_id
        entity_services["template"].create(template)
except Exception as error:
    print(f"Error: {str(error)}")
