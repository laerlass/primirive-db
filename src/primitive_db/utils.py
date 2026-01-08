import json
import os

# Константы согласно критериям (UPPER_SNAKE_CASE)

META_FILE = "db_meta.json"

DATA_DIR = "data"


def save_metadata(metadata):
    """Сохраняет метаданные таблиц в JSON."""

    with open(META_FILE, 'w', encoding='utf-8') as f:

        json.dump(metadata, f, indent=4, ensure_ascii=False)


def load_metadata():
    """Загружает метаданные таблиц из JSON."""

    if not os.path.exists(META_FILE):

        return {}

    with open(META_FILE, 'r', encoding='utf-8') as f:

        return json.load(f)


def ensure_data_dir():
    """Создает папку для данных, если её нет."""

    if not os.path.exists(DATA_DIR):

        os.makedirs(DATA_DIR)


def load_table_data(table_name):
    """
    Загружает данные конкретной таблицы.
    Возвращает список словарей.
    """

    table_file = os.path.join(DATA_DIR, f"{table_name}.json")
    if not os.path.exists(table_file):
        return []
    with open(table_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_table_data(table_name, data):
    """
    Сохраняет список данных в файл талицы.
    """

    table_file = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(table_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
