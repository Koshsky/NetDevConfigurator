# NetDevConfigurator

NetDevConfigurator — это утилита для настройки и управления сетевыми устройствами. Она позволяет обновлять прошивки, настраивать параметры устройств и управлять конфигурациями через удобный интерфейс.

## Установка

Перед началом работы убедитесь, что у вас установлены необходимые зависимости.

### Установка зависимостей

1. Обновите `pip` до последней версии:
    ```bash
    python3 -m pip install --upgrade pip
    ```
2. Установите Poetry для управления зависимостями:
    ```bash
    sudo apt install python3-poetry
    ```
3. Добавьте репозиторий для установки Python 3.11:
    ``` bash
    sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt update
    ```
4. Установите Python 3.11 и необходимые пакеты:
    ```bash
    sudo apt install python3.11
    sudo apt install python3.11-tk
    ```

5. Установите PostgreSQL (если не установлен):
    ```bash
    sudo apt install postgresql
    ```
6. Установите TFTP-сервер (если требуется):
    ```bash
    sudo apt install tftp-hpa
    sudo apt install tftpd-hpa
    ```

### Настройка TFTP-сервера

1. Создайте необходимые директории в папке TFTP-сервера:
    ```bash
    sudo mkdir /srv/tftp/tmp
    sudo mkdir /srv/tftp/firmware
    ```

2. Наполните папку firmware файлами, если вы планируете обновлять сетевые устройства через утилиту.

### Установка NetDevConfigurator

1. Установите Git (если не установлен):
    ```bash
    sudo apt install git
    ```

2. Клонируйте репозиторий проекта:
    ```bash
    git clone https://github.com/Koshekv/NetDevConfigurator
    ```

3. Перейдите в директорию проекта:
    ```bash
    cd NetDevConfigurator/
    ```

4. Укажите версию Python для Poetry:
    ```bash
    poetry env use python3.11
    ```

5. Установите зависимости проекта:
    ```bash
    poetry install
    ```

### Настройка базы данных

Перед использованием утилиты необходимо создать и настроить базу данных:
  ```bash
  sudo -E poetry run python3.11 src/dump.py --restore
  ```

### Использование
Для запуска графического интерфейса используйте команду:
  ```bash
  sudo -E poetry run python3.11 src/configurator-qui.py [-A]
  ```

Для использования утилиты через командную строку выполните:
  ```bash
  sudo -E poetry run python3.11 src/configurator-cli.py
  ```