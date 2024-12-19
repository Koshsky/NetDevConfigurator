from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from internal.database.models import DeviceTemplates, Templates  # Import your models
from internal.database.services import DeviceTemplateService

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/device_registry"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def main():
    # Create a database session
    db_session = SessionLocal()
    
    try:
        # Initialize the service
        service = DeviceTemplateService(db_session)
        
        # Interactive testing menu
        while True:
            print("\n--- Device Template Service Test Menu ---")
            print("1. Push Back Template")
            print("2. Insert Template")
            print("3. Get Device Templates")
            print("4. Delete Template")
            print("5. Exit")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == '1':
                device_id = int(input("Enter device ID: "))
                template_id = int(input("Enter template ID: "))
                result = service.push_back(device_id, template_id)
                print(f"Pushed back template: {result.__dict__}")
            
            elif choice == '2':
                device_id = int(input("Enter device ID: "))
                template_id = int(input("Enter template ID: "))
                ordered_num = int(input("Enter ordered number: "))
                result = service.insert(device_id, template_id, ordered_num)
                print(f"Inserted template: {result.__dict__}")
            
            elif choice == '3':
                device_id = int(input("Enter device ID: "))
                templates = service.get_device_templates(device_id)
                for template in templates:
                    print(template)
            
            elif choice == '4':
                device_template_id = int(input("Enter device template ID to delete: "))
                service.delete_by_id(device_template_id)
                print("Template deleted")
            
            elif choice == '5':
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Always close the session
        db_session.close()

if __name__ == "__main__":
    main()
