import unittest

from bs4 import BeautifulSoup

from parser import Parser
from unittest.mock import patch


class TestParser(unittest.TestCase):
    @patch.object(Parser, 'get_soup')
    def test_get_perfumes_links(self,  mock_get_soup):
        mock_get_soup.return_value = BeautifulSoup("""
        <div class="some-class" data-scroll-id="12345">
            <a href="perfume-link-1"></a>
        </div>
        <div class="some-class" data-scroll-id="67890">
            <a href="perfume-link-2"></a>
        </div>
        """, 'lxml')

        parser = Parser()
        result = parser.get_perfumes_links(1)

        expected_result = ['https://goldapple.ru/perfume-link-1', 'https://goldapple.ru/perfume-link-2']

        self.assertEqual(result, expected_result)

    @patch.object(Parser, 'get_soup')
    def test_get_soup(self, mock_get_soup):
        mock_get_soup.return_value = BeautifulSoup('<html><body></body></html>', 'lxml')

        parser = Parser()
        result = parser.get_soup('https://goldapple.ru/test_url')

        self.assertIsNotNone(result)

    @patch.object(Parser, 'get_soup')
    def test_get_perfumes_data(self, mock_get_soup):
        with open('tests/data/test_get_perfumes_data.html', 'r', encoding='utf-8') as file:
            content = file.read()
        mock_get_soup.return_value = BeautifulSoup(content, 'lxml')

        parser = Parser()
        result = parser.get_perfumes_data('https://goldapple.ru/perfume-link-1')

        expected_result = {
            'url': 'https://goldapple.ru/perfume-link-1',
            'name': 'State Of Mind Sense of humor',
            'price': '8599',
            'rating': '3.8',
            'description': 'В состав набора входит парфюмерная вода.',
            'instruction': 'Только для наружного применения.',
            'country': 'страна происхождения Франция'
        }

        self.assertEqual(result, expected_result)
