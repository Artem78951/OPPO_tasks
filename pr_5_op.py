"""Программа для обработки данных о продуктах из текстового файла."""

from dataclasses import dataclass
from datetime import date
import re


class ProductValidationError(Exception):
    """Исключение, возникающее при ошибке валидации данных продукта."""


@dataclass
class Product:
    """Класс для представления продукта.

    Attributes:
        date (date): Дата продукта
        product_name (str): Название продукта
        quantity (int): Количество
    """

    date: date
    product_name: str
    quantity: int

    def __str__(self):
        """Строковое представление продукта."""
        return f"Дата: {self.date}, Товар: '{self.product_name}', Количество: {self.quantity}"


class ProductParser:
    """Класс для парсинга строк в объекты Product."""

    DATE_PATTERN = re.compile(r"\b(\d{4})\.(\d{2})\.(\d{2})\b")
    QUANTITY_PATTERN = re.compile(r"(?<![-\d.])\b([1-9]\d*)\b(?!\d)(?!\.)")
    NAME_PATTERN = re.compile(r'"([^"]*)"')

    @classmethod
    def _extract_date(cls, line: str) -> date:
        """Извлекает и валидирует дату из строки."""
        match = cls.DATE_PATTERN.search(line)
        if not match:
            raise ProductValidationError("Дата не найдена или "
            "имеет неверный формат (ожидается ГГГГ.ММ.ДД).")
        year, month, day = map(int, match.groups())
        try:
            return date(year, month, day)
        except ValueError as e:
            raise ProductValidationError(f"Некорректная дата: {e}") from e

    @classmethod
    def _extract_quantity(cls, line: str) -> int:
        """Извлекает и валидирует количество из строки."""
        match = cls.QUANTITY_PATTERN.search(line)
        if not match:
            raise ProductValidationError("Количество не найдено или "
            "не является положительным целым числом.")
        return int(match.group(1))

    @classmethod
    def _extract_product_name(cls, line: str) -> str:
        """Извлекает и валидирует название продукта из строки."""
        matches = cls.NAME_PATTERN.findall(line)
        if len(matches) != 1:
            raise ProductValidationError("Название товара должно быть "
            "указано ровно один раз в двойных кавычках.")
        name = matches[0].strip()
        if not name:
            raise ProductValidationError("Название товара не может быть пустым.")
        return name

    @classmethod
    def parse_from_string(cls, line: str) -> Product:
        """Создает объект Product из строки.

        Args:
            line (str): Строка с данными о продукте

        Returns:
            Product: Объект класса Product

        Raises:
            ProductValidationError: Если строка не соответствует формату.
        """
        try:
            product_date = cls._extract_date(line)
            quantity = cls._extract_quantity(line)
            product_name = cls._extract_product_name(line)
            return Product(date=product_date, product_name=product_name, quantity=quantity)
        except ProductValidationError:
            raise
        except Exception as e:
            raise ProductValidationError(f"Неожиданная ошибка при парсинге строки: {e}") from e


def read_file(filename: str) -> list[str]:
    """Читает данные из файла.

    Args:
        filename (str): Имя файла для чтения

    Returns:
        list[str]: Список строк из файла

    Raises:
        FileNotFoundError: Если файл не найден.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()


def filtered_products(all_products: list[Product], min_quantity:\
        int, max_quantity: int) -> list[Product]:
    """Фильтрует продукты по количеству."""
    if min_quantity > max_quantity:
        raise ValueError("Минимальное количество не может быть больше максимального.")
    return [p for p in all_products if min_quantity <= p.quantity <= max_quantity]


def sort_products_by_date(products: list[Product]) -> list[Product]:
    """Сортирует продукты по дате (по возрастанию)."""
    return sorted(products, key=lambda p: p.date)


def display_products(products: list[Product]) -> None:
    """Выводит список продуктов в консоль."""
    for product in products:
        print(product)


# --- Основная логика ---
def process_and_collect_products(lines: list[str]) -> tuple[list[Product],\
        list[tuple[int, str, str]]]:
    """Обрабатывает строки, возвращает продукты и список ошибок."""
    valid_products = []
    errors = []
    for idx, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            product = ProductParser.parse_from_string(line)
            valid_products.append(product)
        except ProductValidationError as e:
            errors.append((idx, line, str(e)))
    return valid_products, errors


def handle_user_choice(products: list[Product]) -> None:
    """Обрабатывает выбор пользователя из меню и выполняет соответствующее действие."""
    print("\n1 — Вывести товары, отсортированные по дате")
    print("2 — Вывести товары, отфильтрованные по количеству")
    try:
        choice = int(input("Выберите действие: "))
    except ValueError:
        print("Неверный выбор.")
        return

    if choice == 1:
        sorted_products = sort_products_by_date(products)
        print("\nТовары, отсортированные по дате:")
        display_products(sorted_products)
    elif choice == 2:
        try:
            min_quantity = int(input("Введите минимальное количество: "))
            max_quantity = int(input("Введите максимальное количество: "))
            filtered = filtered_products(products, min_quantity, max_quantity)
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
            return

        if not filtered:
            print("Нет товаров, удовлетворяющих условиям фильтрации.")
        else:
            print("\nОтфильтрованные товары:")
            display_products(filtered)
    else:
        print("Неверный выбор.")


def main():
    """Основная функция программы."""
    filename = "primer1_for_Pr3.txt"

    try:
        lines = read_file(filename)
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        return

    all_products, errors = process_and_collect_products(lines)

    # Вывод обработанных продуктов
    if all_products:
        for p in all_products:
            print(p)
    else:
        print("Ни один товар не был успешно обработан.")

    # Вывод ошибок
    if errors:
        print("\nОшибки при обработке строк:")
        for line_num, line, error in errors:
            print(f"Строка {line_num}: '{line}' → Ошибка: {error}")

    if not all_products:
        return

    handle_user_choice(all_products)


if __name__ == "__main__":
    main()
