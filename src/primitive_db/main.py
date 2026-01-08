#!/usr/bin/env python3

"""

Main entry point for the primitive database application.

"""

import prompt


def main():
    """

    Main function to run the application.

    """
    print("DB project is running!")

    # Пример работы с библиотекой prompt согласно заданию [cite: 486]
    name = prompt.string('May I have your name? ')
    print(f"Hello, {name}!")


if __name__ == "__main__":
    main()
