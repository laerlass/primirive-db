import shlex

import prompt
from prettytable import PrettyTable

from .core import create_table, delete, drop_table, insert, list_tables, select, update
from .decorators import create_cacher
from .parser import parse_condition, parse_values


def print_help():
    """Выводит справку по командам"""

    print("\n*** База данных: Список команд ***")

    print("  create_table <имя> <колонки...>")

    print("  list_tables")

    print("  drop_table <имя>")

    print("  insert into <имя> values (<значения...>)")

    print("  select from <имя> [where <колонки>=<значение>]")

    print("  update <имя> set <кол1>=<вал1> where <кол2>=<вал2>")

    print("  delete from <имя> where <кол>=<вал>")

    print("  help - справка")

    print("  exit - выход")


def run():

    print_help()

    get_cache = create_cacher()  # Инициализируем кэш (замыкание)

    while True:

        try:

            raw_input = prompt.string(">>> Введите команду: ")

            if not raw_input:

                continue

            tokens = shlex.split(raw_input)

            command = tokens[0].lower()

            args = tokens[1:]

            if command == "exit":

                print("До свидания!")

                break

            elif command == "help":

                print_help()

            elif command == "list_tables":

                tables = list_tables()

                print("Список таблиц:", ", ".join(
                    tables) if tables else "пусто")

            elif command == "create_table":

                if len(args) < 2:

                    print("Ошибка: укажите имя и колонки (напр. name:str)")

                    continue

                table_name = args[0]

                cols = {c.split(":")[0]: c.split(":")[1]
                        for c in args[1:] if ":" in c}

                create_table(table_name, cols)

            elif command == "drop_table":

                if args:

                    drop_table(args[0])

            elif command == "insert":

                if len(args) >= 4 and args[0] == "into" and args[2] == "values":

                    table_name = args[1]

                    values = parse_values(" ".join(args[3:]))

                    insert(table_name, values)

            elif command == "select":

                if len(args) < 2 or args[0] != "from":

                    print("Ошибка. Пример: select from users [where id=1]")

                    continue

                table_name = args[1]

                where_clause = None

                if len(args) > 3 and args[2] == "where":

                    where_clause = parse_condition(args[3])

                # Работаем через кэш

                cache_key = f"{table_name}_{where_clause}"

                results = get_cache(
                    cache_key, lambda: select(table_name, where_clause))

                if results:

                    table = PrettyTable()

                    table.field_names = list(results[0].keys())

                    for row in results:

                        table.add_row(list(row.values()))

                    print(table)

                else:

                    print("Записей не найдено.")

            elif command == "update":

                if len(args) >= 5 and args[1] == "set" and args[3] == "where":

                    table_name = args[0]

                    set_c = parse_condition(args[2])

                    where_c = parse_condition(args[4])

                    update(table_name, set_c, where_c)

            elif command == "delete":

                if len(args) >= 4 and args[0] == "from" and args[2] == "where":

                    table_name = args[1]

                    where_c = parse_condition(args[3])

                    delete(table_name, where_c)

            else:

                print(f"Неизвестная команда: {command}")

        except EOFError:

            break

        except Exception as e:

            print(f"Ошибка: {e}")
