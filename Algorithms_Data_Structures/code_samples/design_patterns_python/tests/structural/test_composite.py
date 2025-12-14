import unittest

from design_patterns.structural.composite import (Check, CompositeOrder,
                                                  Device, ProductPackage)


class CompositeTestCase(unittest.TestCase):

    def test_00_init_composite(self):
        CompositeTestCase.order = CompositeOrder()

    def test_01_product_package(self):
        price1, price2 = 699.99, 599.99
        weight1, weight2 = 172, 179
        i_phone = Device(
            name='iPhone 14',
            weight=weight1,
            price=price1)
        google_pixel = Device(
            name='Pixel 7',
            weight=weight2,
            price=price2)

        phone_package = ProductPackage()
        phone_package.add(i_phone)
        phone_package.add(google_pixel)

        self.assertEqual(phone_package.price_total, price1 + price2)
        self.assertEqual(phone_package.weight_total, weight1 + weight2)
        self.assertEqual(len(phone_package), 2)

        CompositeTestCase.order.add(phone_package)

    def test_02_product_bad_index(self):
        order = self.order

        self.assertEqual(len(order), 1)

        with self.assertRaises(KeyError):
            order.remove(10)
        order.remove(2)

    def test_03_order_checkout(self):
        order = self.order
        check = order.checkout()

        self.assertIsInstance(check, Check)


if __name__ == '__main__':
    unittest.main()
