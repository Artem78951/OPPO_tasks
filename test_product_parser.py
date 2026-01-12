import unittest
from datetime import date
from Pr_3_OP import Product, ProductParser, ProductValidationError

class TestProductParser(unittest.TestCase):

    def test_valid_line(self):
        line = '2023.12.01 "Творог" 42'
        product = ProductParser.parse_from_string(line)
        self.assertEqual(product.date, date(2023, 12, 1))
        self.assertEqual(product.product_name, "Творог")
        self.assertEqual(product.quantity, 42)

    def test_invalid_date(self):
        with self.assertRaises(ProductValidationError):
            ProductParser.parse_from_string('2023.13.01 "Хлеб" 5')

    def test_missing_name(self):
        with self.assertRaises(ProductValidationError):
            ProductParser.parse_from_string('2023.01.01 10')

    def test_zero_quantity(self):
        with self.assertRaises(ProductValidationError):
            ProductParser.parse_from_string('2023.01.01 "Молоко" 0')

    def test_empty_name(self):
        with self.assertRaises(ProductValidationError):
            ProductParser.parse_from_string('2023.01.01 "" 5')

    def test_negative_quantity_not_matched(self):
        with self.assertRaises(ProductValidationError):
            ProductParser.parse_from_string('2023.01.01 "Соль" -5')

    def test_multiple_names(self):
        with self.assertRaises(ProductValidationError):
            ProductParser.parse_from_string('2023.01.01 "Молоко" "Сыр" 10')

    def test_decimal_quantity(self):
        with self.assertRaises(ProductValidationError):
            ProductParser.parse_from_string('2023.01.01 "Молоко" 10.5')


class TestProduct(unittest.TestCase):

    def test_product_str(self):
        p = Product(date=date(2024, 1, 1), product_name="Йогурт", quantity=7)
        self.assertIn("2024-01-01", str(p))
        self.assertIn("Йогурт", str(p))
        self.assertIn("7", str(p))


if __name__ == '__main__':
    unittest.main()