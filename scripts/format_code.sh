#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Форматирование кода...${NC}\n"

# Форматирование с помощью autopep8
echo -e "${YELLOW}Применяем autopep8...${NC}"
poetry run autopep8 --in-place --aggressive --aggressive --max-line-length 88 src tests

# Форматирование с помощью black
echo -e "\n${YELLOW}Применяем black...${NC}"
poetry run black src tests --line-length 88 --preview

# Сортировка импортов
echo -e "\n${YELLOW}Сортируем импорты с помощью isort...${NC}"
poetry run isort src tests

# Проверка стиля кода с помощью flake8
echo -e "\n${YELLOW}Проверяем стиль кода с помощью flake8...${NC}"
poetry run flake8 --max-line-length=88 --extend-ignore=E203,E501 src tests

echo -e "\n${GREEN}Форматирование завершено!${NC}"
