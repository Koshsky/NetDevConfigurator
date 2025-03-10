# NetDevConfigurator

NetDevConfigurator — это утилита для настройки и управления сетевыми устройствами. Она позволяет обновлять прошивки, настраивать параметры устройств и управлять конфигурациями через удобный интерфейс.

## Возможности

* Обновление прошивок сетевых устройств.
* Настройка параметров сетевых устройств.
* Управление конфигурациями.
* Удобный графический интерфейс (GUI) и интерфейс командной строки (CLI).

## Установка

NetDevConfigurator требует Python 3.11, PostgreSQL и TFTP-сервер (для обновления прошивки).


### Шаг 1: Установка зависимостей

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-tk postgresql tftp-hpa tftpd-hpa git python3-poetry
```


### Шаг 2: Настройка TFTP-сервера

1. Создайте необходимые директории в папке TFTP-сервера:
    ```bash
    sudo mkdir /srv/tftp/tmp /srv/tftp/firmware
    ```

2. Наполните папку firmware файлами, если вы планируете обновлять сетевые устройства через утилиту.

### Шаг 3: Установка NetDevConfigurator

```bash
git clone https://github.com/Koshekv/NetDevConfigurator
cd NetDevConfigurator
poetry env use python3.11
poetry install
```

### Шаг 4: Настройка базы данных

  ```bash
  sudo -E poetry run python3.11 src/dump.py --restore
  ```

## Запуск

### Графический интерфейс (GUI)

  ```bash
  sudo -E poetry run python3.11 src/configurator-gui.py [-A]
  ```

### Интерфейс командной строки (CLI)
  ```bash
  sudo -E poetry run python3.11 src/configurator-cli.py
  ```

## Примеры

бла-бла-бла

