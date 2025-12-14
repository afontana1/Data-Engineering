import unittest

from design_patterns.structural.flyweight import Flyweight


class FlyweightTestCase(unittest.TestCase):

    def test_00_init_flyweight(self):
        FlyweightTestCase.flyweight = Flyweight()

    def test_01_test_reference(self):
        f1 = Flyweight(1, 'Storage')
        f2 = Flyweight(1, 'Storage')

        self.assertTrue(f1 == f2)
        self.assertTrue(f1 is f2)
        self.assertEqual(id(f1), id(f2))

    def test_02_test_reference(self):
        f1 = Flyweight(1, 'Storage')
        f2 = Flyweight(2, 'Storage')

        self.assertFalse(f1 == f2)
        self.assertFalse(f1 is f2)
        self.assertNotEqual(id(f1), id(f2))


if __name__ == '__main__':
    unittest.main()
