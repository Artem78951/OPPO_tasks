""" Программа для обработки данных о продуктах из текстового файла."""

from dataclasses import dataclass
from datetime import date
import re


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

    def str(self):
        """Строковое представление продукта."""
        return f"Дата: {self.date}, Товар: '{self.product_name}', Количество: {self.quantity}"

class ProductParser:
    """Класс для парсинга строк в объекты Product."""

    @staticmethod
    def _extract_date(line):
        """Извлекает дату из строки."""
        date_match = re.search(r"\b\d{4}\.\d{2}\.\d{2}\b", line)
        if date_match:
            date_str = date_match.group()
            # Преобразуем строку в объект date
            return date_str
        return None

    @staticmethod
    def _extract_quantity(line):
        """Извлекает количество из строки."""
        quantity_match = re.search(r"(?<!\.)\b([1-9]\d*)\b(?!\.)", line)
        if quantity_match:
            return int(quantity_match.group())
        return None

    @staticmethod
    def _extract_product_name(line):
        """Извлекает название продукта из строки."""
        name_match = re.search(r'"([^"]*)"', line)
        if name_match:
            return name_match.group(1).strip()
        return None

    @classmethod
    def parse_from_string(cls, line):
        """Создает объект Product из строки.

        Args:
            line (str): Строка с данными о продукте

        Returns:
            Product: Объект класса Product
        """
        date = cls._extract_date(line)
        quantity = cls._extract_quantity(line)
        product_name = cls._extract_product_name(line)


        return Product(date=date, product_name=product_name, quantity=quantity)


def read_file(filename):
    """Читает данные из файла.

    Args:
        filename (str): Имя файла для чтения

    Returns:
        list: Список строк из файла
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()


def filtered_products(all_products, min_quantity, max_quantity):
    """Фильтрует продукты по количеству.

    Args:
        all_products (list): Список объектов Products
        min_quantity (int): Минимальное количество
        max_quantity (int): Максимальное количество

    Returns:
        list: Отфильтрованный список продуктов
    """
    formatted_products = []
    for product in all_products:
        if min_quantity <= product.quantity <= max_quantity:
            formatted_products.append(product)
    return formatted_products


def sort_products_by_date(products: list[Product]) -> list[Product]:
    """Сортирует продукты по дате (по возрастанию).

    Args:
        products (list[Product]): Список продуктов.

    Returns:
        list[Product]: Отсортированный список продуктов.
    """
    return sorted(products, key=lambda p: p.date)


def display_products(products: list[Product]) -> None:
    """Выводит список продуктов в консоль.

    Args:
        products (list[Product]): Список объектов Product для вывода.
    """
    for product in products:
        print(product)


def main():
    """Основная функция программы."""
    filename = "products.txt"

    # Читаем данные из файла
    lines = read_file(filename)
    all_products = []

    # Обрабатываем данные
    for line in lines:
        product_obj = ProductParser.parse_from_string(line)
        all_products.append(product_obj)
        print(product_obj)

    # Меню выбора действия
    print("\n1 — Вывести товары, отсортированные по дате")
    print("2 — Вывести товары, отфильтрованные по количеству")
    try:
        choice = int(input("Выберите действие: "))
    except ValueError:
        print("Неверный выбор.")
        return

if choice == 1:
        sorted_products = sort_products_by_date(all_products)
        print("\nТовары, отсортированные по дате:")
        display_products(sorted_products)

    elif choice == 2:
        try:
            min_quantity = int(input("Введите минимальное количество: "))
            max_quantity = int(input("Введите максимальное количество: "))
        except ValueError:
            print("Количество должно быть целым числом.")
            return

        filtered = filtered_products(all_products, min_quantity, max_quantity)
        if not filtered:
            print("Нет товаров, удовлетворяющих условиям фильтрации.")
        else:
            print("\nОтфильтрованные товары:")
            display_products(filtered)

    else:
        print("Неверный выбор.")


if name == "main":
    main()
