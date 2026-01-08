def parse_values(values_str):
    """

    Парсит строку значений вида '(val1, val2, ...)' в список строк.

    Убирает скобки и разбивает по запятым.

    """

    # Удаляем скобки по краям

    clean_str = values_str.strip("()")

    # Разбиваем по запятой и убираем лишние пробелы и кавычки у каждого значения

    values = [v.strip().strip('"').strip("'") for v in clean_str.split(",")]

    return values


def parse_condition(condition_str):
    """

    Парсит строку условия вида 'col=val' в кортеж (col, val).

    Пример: 'age=25' -> ('age', '25')

    """

    if "=" not in condition_str:

        return None, None

    col, val = condition_str.split("=", 1)

    return col.strip(), val.strip().strip('"').strip("'")
