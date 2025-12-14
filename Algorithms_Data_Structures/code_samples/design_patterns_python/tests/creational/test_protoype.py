import unittest
from unicodedata import decimal

from design_patterns.creational.prototype import Prototype


class PrototypeTestCase(unittest.TestCase):

    def test_00_init_prototype(self):
        PrototypeTestCase.prototype = Prototype()
        self.prototype.load()

        self.assertEqual(len(self.prototype.cache), 3)
        # self.assertAlmostEqual(decimal=0)

    def test_01_test_rect_shape(self):
        shape1 = self.prototype.get_shape(1)

        shape1.width = 5
        shape1.height = 6

        self.assertEqual(shape1.get_area(), 30)

    def test_02_test_circle_shape(self):
        shape3 = self.prototype.get_shape(3)

        shape3.radius = 15

        self.assertEqual(int(shape3.get_area()), 706)


if __name__ == '__main__':
    unittest.main()
