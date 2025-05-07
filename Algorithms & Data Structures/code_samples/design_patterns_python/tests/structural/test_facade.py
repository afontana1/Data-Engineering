import unittest

from design_patterns.structural.composite import Check
from design_patterns.structural.facade import Facade


class FacadeTestCase(unittest.TestCase):

    def test_00_init_facade(self):
        FacadeTestCase.facade = Facade()

    def test_01_test_do_facade(self):
        check = self.facade.do()

        self.assertIsInstance(check, Check)


if __name__ == '__main__':
    unittest.main()
