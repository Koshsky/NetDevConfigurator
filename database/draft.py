# demo.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.company_service import CompanyService
from services.device_service import DeviceService
from services.firmware_service import FirmwareService
from models.base import Base  # Предполагается, что у вас есть файл base.py
from models.company import Company
from models.device import Device
from models.firmware import Firmware

# Настройки подключения к базе данных
DATABASE_URL = 'sqlite:///example.db'  # Замените на вашу строку подключения

# Создание движка и сессии
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def main():
    # Создаем сессию
    session = Session()

    # Инициализируем сервисы
    company_service = CompanyService(session)
    device_service = DeviceService(session)
    firmware_service = FirmwareService(session)

    # Демонстрация работы с CompanyService
    print("Создание компании...")
    company = company_service.create_company(name="Tech Corp", address="123 Tech Lane")
    print(f"Создана компания: {company.id}, {company.name}, {company.address}")

    print("\nПолучение всех компаний...")
    companies = company_service.get_all_companies()
    for c in companies:
        print(f"Компания: {c.id}, {c.name}, {c.address}")

    print("\nОбновление компании...")
    updated_company = company_service.update_company(company.id, address="456 New Tech Lane")
    print(f"Обновленная компания: {updated_company.id}, {updated_company.name}, {updated_company.address}")

    print("\nУдаление компании...")
    company_service.delete_company(company.id)
    print("Компания удалена.")

    # Демонстрация работы с DeviceService
    print("\nСоздание устройства...")
    device = device_service.create_device(name="Device A", company_id=company.id)
    print(f"Создано устройство: {device.id}, {device.name}")

    print("\nПолучение всех устройств...")
    devices = device_service.get_all_devices()
    for d in devices:
        print(f"Устройство: {d.id}, {d.name}")

    print("\nОбновление устройства...")
    updated_device = device_service.update_device(device.id, name="Device A Updated")
    print(f"Обновленное устройство: {updated_device.id}, {updated_device.name}")

    print("\nУдаление устройства...")
    device_service.delete_device(device.id)
    print("Устройство удалено.")

    # Демонстрация работы с FirmwareService
    print("\nСоздание прошивки...")
    firmware = firmware_service.create_firmware(version="1.0.0")
    print(f"Создана прошивка: {firmware.id}, {firmware.version}")

    print("\nПолучение всех прошивок...")
    firmwares = firmware_service.get_all_firmwares()
    for f in firmwares:
        print(f"Прошивка: {f.id}, {f.version}")

    print("\nОбновление прошивки...")
    updated_firmware = firmware_service.update_firmware(firmware.id, version="1.0.1")
    print(f"Обновленная прошивка: {updated_firmware.id}, {updated_firmware.version}")

    print("\nУдаление прошивки...")
    firmware_service.delete_firmware(firmware.id)
    print("Прошивка удалена.")

    # Закрываем сессию
    session.close()

if __name__ == "__main__":
    main()