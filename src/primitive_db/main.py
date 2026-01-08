#!/usr/bin/env python3

from . import engine


def main():
    """

    Точка входа, вызывающая основной цикл движка.

    """

    try:
        engine.run()
    except KeyboardInterrupt:
        print("\nПрограмма принудительно завершена.")


if __name__ == "__main__":
    main()
