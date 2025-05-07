import unittest

from design_patterns.structural.adapter import Adapter, NewsArticle


class AdapterTestCase(unittest.TestCase):

    def test_00_init_adapter(self):
        AdapterTestCase.adapter = Adapter()
        AdapterTestCase.sample_news_json = '''
        {
            "created": "01/01/2022, 03:00",
            "title": "Amazing content",
            "text": "This is good content",
            "published": "02/01/2022, 00:00"
        }
        '''
        AdapterTestCase.sample_news_xml = '''
        <NewsArticle>
            <created>01/01/2022, 03:00</created>
            <title>Amazing content</title>
            <text>This is good content</text>
            <published>02/01/2022, 00:00</published>
        </NewsArticle>
        '''

    def test_01_dataclasses(self):
        test_text = 'Test Content'
        article = NewsArticle(text='Test Content')

        self.assertEqual(article.text, test_text)

    def test_02_json_to_obj(self):
        article = self.adapter.json_to_obj(NewsArticle, self.sample_news_json)

        self.assertIsInstance(article, NewsArticle)

        self.assertEqual(article.title, 'Amazing content')
        self.assertEqual(article.text, 'This is good content')

    def test_03_xml_to_obj(self):
        article = self.adapter.xml_to_obj(NewsArticle, self.sample_news_xml)

        self.assertIsInstance(article, NewsArticle)
        self.assertEqual(article.text, 'This is good content')

    def test_03_xml_parse_error(self):
        bad_xml = self.sample_news_xml.replace('NewsArticle', 'BadNewsArticle')
        with self.assertRaises(ValueError):
            self.adapter.xml_to_obj(NewsArticle, bad_xml)

    def test_04_xml_parse_error(self):
        bad_xml = (self.sample_news_xml * 2)
        with self.assertRaises(Exception):
            self.adapter.xml_to_obj(NewsArticle, bad_xml)

    def test_05_obj_to_json(self):
        article = NewsArticle(title='test title', text='test string')

        parse_article = self.adapter.json_parser.to_text(article)

        self.assertEqual('"title": "test title"' in parse_article, True)
        self.assertEqual('"text": "test string"' in parse_article, True)

    def test_06_obj_to_xml(self):
        article = NewsArticle(title='test title', text='test string')

        parse_article = self.adapter.xml_parser.to_text(article)

        self.assertEqual('<title>test title</title>' in parse_article, True)
        self.assertEqual('<text>test string</text>' in parse_article, True)

    def test_07_xml_to_json(self):
        parse_article = self.adapter.xml_to_json(NewsArticle, self.sample_news_xml)

        self.assertEqual('"title": "Amazing content"' in parse_article, True)
        self.assertEqual('"text": "This is good content"' in parse_article, True)

    def test_08_json_to_xml(self):
        parse_article = self.adapter.json_to_xml(NewsArticle, self.sample_news_json)

        self.assertEqual('<title>Amazing content</title>' in parse_article, True)
        self.assertEqual('<text>This is good content</text>' in parse_article, True)


if __name__ == '__main__':
    unittest.main()
