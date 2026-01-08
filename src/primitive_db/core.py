import json
import os

from .decorators import confirm_action, handle_db_errors, log_time
from .utils import (
    DATA_DIR,
    ensure_data_dir,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


@handle_db_errors
def create_table(table_name, columns):
    metadata = load_metadata()
    if table_name in metadata:
        print(f"Ошибка: Таблица '{table_name}' уже существует.")
        return False
    table_struct = {"id": "int"}
    table_struct.update(columns)
    metadata[table_name] = {"columns": table_struct}
    save_metadata(metadata)
    ensure_data_dir()
    table_file = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(table_file, 'w', encoding='utf-8') as f:
        json.dump([], f)
    print(f"Таблица '{table_name}' успешно создана.")
    return True


@confirm_action
@handle_db_errors
def drop_table(table_name):
    metadata = load_metadata()
    if table_name not in metadata:
        print(f"Ошибка: Таблица '{table_name}' не найдена.")
        return False
    del metadata[table_name]
    save_metadata(metadata)
    table_file = os.path.join(DATA_DIR, f"{table_name}.json")
    if os.path.exists(table_file):
        os.remove(table_file)
    print(f"Таблица '{table_name}' удалена.")
    return True


@log_time
@handle_db_errors
def insert(table_name, values):
    metadata = load_metadata()
    if table_name not in metadata:
        print(f"Ошибка: Таблица '{table_name}' не существует.")
        return False
    columns = metadata[table_name]["columns"]
    col_names = [c for c in columns.keys() if c != "id"]
    if len(values) != len(col_names):
        print(
            f"Ошибка: Ожидается {len(col_names)} значений, получено {len(values)}.")
        return False
    data = load_table_data(table_name)
    new_id = data[-1]["id"] + 1 if data else 1
    new_record = {"id": new_id}
    for col_name, value_str in zip(col_names, values):
        col_type = columns[col_name]
        if col_type == "int":
            new_record[col_name] = int(value_str)
        elif col_type == "bool":
            new_record[col_name] = value_str.lower() in ("true", "1", "yes")
        else:
            new_record[col_name] = value_str
    data.append(new_record)
    save_table_data(table_name, data)
    print(f"Запись с ID={new_id} добавлена.")
    return True


@log_time
@handle_db_errors
def select(table_name, where_clause=None):
    metadata = load_metadata()
    if table_name not in metadata:
        print(f"Ошибка: Таблица '{table_name}' не найдена.")
        return []
    data = load_table_data(table_name)
    if not where_clause:
        return data
    filter_col, filter_val = where_clause
    return [row for row in data if str(row.get(filter_col)) == filter_val]


@handle_db_errors
def update(table_name, set_clause, where_clause):
    metadata = load_metadata()
    data = load_table_data(table_name)
    set_col, set_val = set_clause
    where_col, where_val = where_clause
    col_type = metadata[table_name]["columns"].get(set_col)
    updated_count = 0
    for row in data:
        if str(row.get(where_col)) == where_val:
            if col_type == "int":
                row[set_col] = int(set_val)
            elif col_type == "bool":
                row[set_col] = set_val.lower() in ("true", "1", "yes")
            else:
                row[set_col] = set_val
            updated_count += 1
    if updated_count > 0:
        save_table_data(table_name, data)
        print(f"Обновлено строк: {updated_count}")
    return True


@confirm_action
@handle_db_errors
def delete(table_name, where_clause):
    data = load_table_data(table_name)
    where_col, where_val = where_clause
    new_data = [row for row in data if str(row.get(where_col)) != where_val]
    if len(data) != len(new_data):
        save_table_data(table_name, new_data)
        print(f"Удалено строк: {len(data) - len(new_data)}")
    return True


def list_tables():
    return list(load_metadata().keys())
