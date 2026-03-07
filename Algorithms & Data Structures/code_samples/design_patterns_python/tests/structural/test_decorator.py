import unittest

from design_patterns.structural.decorator import Data, File, GZIPDecorator


class DecoratorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_name = 'test_file.txt'
        cls.test_data = 'This is some very good test data'
        data = Data(cls.test_data)
        cls.decorator = GZIPDecorator(data)

    def test_00_init_decorator(self):
        self.assertIsInstance(self.decorator, GZIPDecorator)
        self.assertIsInstance(self.decorator.read(), Data)

    def test_01_test_file_create(self):
        file = File(self.file_name)
        data = Data(self.test_data)
        file.write(data)

        read_file = File(self.file_name, create=False)
        read_data = read_file.data

        self.assertEqual(read_data.text, data.text)

    def test_02_test_data_types(self):
        data = Data(self.test_data)

        self.assertIsInstance(data.text, str)
        self.assertIsInstance(data.blob, bytes)

    def test_03_test_data_value(self):
        data = Data(self.test_data)

        self.assertEqual(data.text, self.test_data)

    def test_04_test_compression(self):
        data = Data(self.test_data * 100)
        compressor = GZIPDecorator(Data(self.test_data * 100))
        compressed_data = compressor.read()

        self.assertGreater(data.size, compressed_data.size)

    def test_05_test_decompression(self):
        data = Data(self.test_data)
        compressor = GZIPDecorator(Data(self.test_data))
        compressed_data = compressor.read()
        compressor = GZIPDecorator(compressed_data, True)
        decompressed_data = compressor.read()

        self.assertEqual(data.text, decompressed_data.text)


if __name__ == '__main__':
    unittest.main()
