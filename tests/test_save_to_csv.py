import unittest

from unittest.mock import patch

from save_to_csv import SaveCSV


class TestSaveCSV(unittest.TestCase):

    @patch('save_to_csv.Parser')
    def test_save_to_csv(self, mock_parser_class):

        mock_pages = 2
        save_csv_instance = SaveCSV(mock_pages)

        mock_parser = mock_parser_class.return_value
        mock_parser.get_perfumes_links.side_effect = [
            ["https://goldapple.ru/perfume1"],
            ["https://goldapple.ru/perfume2"],
            [],
        ]

        perfume1_data = {
            'url': 'https://goldapple.ru/perfume1',
            'name': 'Perfume 1',
            'price': '1000',
            'rating': '4.5',
            'description': 'Description of Perfume 1',
            'instruction': 'Instruction for Perfume 1',
            'country': 'Russia'
        }
        perfume2_data = {
            'url': 'https://goldapple.ru/perfume2',
            'name': 'Perfume 2',
            'price': '2000',
            'rating': '4.7',
            'description': 'Description of Perfume 2',
            'instruction': 'Instruction for Perfume 2',
            'country': 'USA'
        }
        mock_parser.get_perfumes_data.side_effect = [perfume1_data, perfume2_data]

        save_csv_instance.save_csv()

        expected_output = (
                'url|name|price|rating|description|instruction|country\n' +
                'https://goldapple.ru/perfume1|Perfume 1|1000|4.5|Description of Perfume 1|Instruction for Perfume '
                '1|Russia\n' +
                'https://goldapple.ru/perfume2|Perfume 2|2000|4.7|Description of Perfume 2|Instruction for Perfume '
                '2|USA\n'
        )

        with open("goldapple.csv", "r", encoding="utf-8") as f:
            actual_output = f.read()

        self.assertEqual(actual_output, expected_output)
