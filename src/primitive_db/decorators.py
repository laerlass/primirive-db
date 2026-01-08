import json
import time
from functools import wraps


def handle_db_errors(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:

            return func(*args, **kwargs)

        except (json.JSONDecodeError, ValueError) as e:

            print(f"Ошибка данных: {e}. Попробуйте пересоздать таблицу.")

        except Exception as e:

            print(f"Произошла системная ошибка: {e}")

        return None

    return wrapper


def confirm_action(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        confirm = input(
            f"Вы уверены, что хотите выполнить '{func.__name__}'? (y/n): ")

        if confirm.lower() == 'y':

            return func(*args, **kwargs)

        print("Действие отменено.")

        return False

    return wrapper


def log_time(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.monotonic()

        result = func(*args, **kwargs)

        duration = time.monotonic() - start

        print(
            f"Функция <{func.__name__}> выполнилась за {duration:.4f} сек.")

        return result

    return wrapper


def create_cacher():
    """Замыкание для кэширования результатов select."""

    cache = {}

    def cache_result(key, value_func):

        if key in cache:

            print("[КЭШ] Возврат данных из памяти")

            return cache[key]

        result = value_func()

        cache[key] = result

        return result

    return cache_result
