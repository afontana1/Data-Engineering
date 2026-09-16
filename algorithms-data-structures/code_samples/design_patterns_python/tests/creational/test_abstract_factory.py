import unittest

from design_patterns.creational.abstract_factory import AbstractFactory


class AbstractFactoryTestCase(unittest.TestCase):

    def test_00_init_factory(self):
        VictorianFurnitureFactory = AbstractFactory.new(style='victorian')
        ModernFurnitureFactory = AbstractFactory.new(style='modern')
        ArtDecoFurnitureFactory = AbstractFactory.new(style='art_deco')

        self.assertEqual(VictorianFurnitureFactory.style.value, 'victorian',
                         'Incorrect Factory style')
        self.assertEqual(ModernFurnitureFactory.style.value, 'modern',
                         'Incorrect Factory style')
        self.assertEqual(ArtDecoFurnitureFactory.style.value, 'art_deco',
                         'Incorrect Factory style')

    def test_01_bad_style_factory(self):
        with self.assertRaises(Exception):
            AbstractFactory.new(style='punk')

    def test_02_style_furniture_check(self):
        VictorianFurnitureFactory = AbstractFactory.new(style='victorian')

        chair = VictorianFurnitureFactory.make_chair()

        self.assertEqual(chair.style.value, 'victorian',
                         'Incorrect Furniture style')


if __name__ == '__main__':
    unittest.main()
