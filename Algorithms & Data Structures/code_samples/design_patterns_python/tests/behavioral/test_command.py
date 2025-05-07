import unittest

from design_patterns.behavioral.command import Command


class CommandTestCase(unittest.TestCase):

    def test_00_init_adapter(self):
        CommandTestCase.command = Command()
