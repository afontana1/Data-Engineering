import unittest
from unicodedata import decimal

from design_patterns.creational.singleton import DatabasePrototype


class PrototypeTestCase(unittest.TestCase):

    def test_00_init_prototype(self):
        PrototypeTestCase.db = DatabasePrototype.instance()

        self.assertIsInstance(self.db, DatabasePrototype, 'Instance is not of DatabasePrototype')

    def test_01_init_prototype_fail(self):
        with self.assertRaises(Exception):
            bad_db = DatabasePrototype()

    def test_02_test_query(self):

        query = 'SELECT * FROM Customers;'

        result = self.db.query(query)

        self.assertEqual(result, f'Result for {query}', 'Incorrect db query result')


if __name__ == '__main__':
    unittest.main()
