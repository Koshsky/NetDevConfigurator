#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Запуск проверок кода...${NC}\n"

# Проверка форматирования с помощью black
echo -e "${YELLOW}Проверка форматирования (black)...${NC}"
poetry run black --check --line-length 88 --preview src tests
BLACK_RESULT=$?

# Сортировка импортов
echo -e "\n${YELLOW}Проверка сортировки импортов (isort)...${NC}"
poetry run isort --check-only src tests
ISORT_RESULT=$?

# Проверка типов
echo -e "\n${YELLOW}Проверка типов (mypy)...${NC}"
poetry run mypy src
MYPY_RESULT=$?

# Проверка стиля кода
echo -e "\n${YELLOW}Проверка стиля кода (flake8)...${NC}"
poetry run flake8 --max-line-length=88 --extend-ignore=E203,E501 src tests
FLAKE8_RESULT=$?

# Проверка с помощью pylint
echo -e "\n${YELLOW}Проверка кода (pylint)...${NC}"
poetry run pylint --max-line-length=88 src tests
PYLINT_RESULT=$?

# Проверка безопасности
echo -e "\n${YELLOW}Проверка безопасности (bandit)...${NC}"
poetry run bandit -r src
BANDIT_RESULT=$?

# Подсчет общего результата
TOTAL_RESULT=$((BLACK_RESULT + ISORT_RESULT + MYPY_RESULT + FLAKE8_RESULT + PYLINT_RESULT + BANDIT_RESULT))

if [ $TOTAL_RESULT -eq 0 ]; then
    echo -e "\n${GREEN}Все проверки пройдены успешно!${NC}"
else
    echo -e "\n${RED}Проверки завершились с ошибками.${NC}"
    exit 1
fi
