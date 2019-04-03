import unittest
from EtlChallengeModule.etl_module_data_manipulation import *
from EtlChallengeModule.etl_module_utils import *


class TestCase(unittest.TestCase):

    def setUp(self):
        print('Creating test set up')
        self.test_path = 'test_file.txt'
        self.na = '-'
        self.test_text_data = TxtData(self.test_path, self.na)
        self.test_text_data.load(0)

    def test_get_headers(self):
        self.assertEqual(self.test_text_data.get_headers(0),
                         ['number', 'class', 'relevancy', 'comma-num', 'Nan',
                          'cents'])

    def test_one_hot_encoding(self):
        self.test_text_data.data_to_one_hot_encoding(['class'])
        for row in self.test_text_data.data:
            self.assertIsInstance(row[1], type([]))

    def test_drop_nas(self):
        self.test_text_data.drop_na()
        test_var = [['number', 'class', 'relevancy', 'comma-num', 'Nan',
                     'cents'],
                    ['three', 'B', 'yes', '10,1', 'not', '15000'],
                    ['three', 'C', 'yes', '10,1', 'not', '15000']]
        self.assertEqual(self.test_text_data.get_data_matrix(), test_var)

    def test_cents_to_eur(self):
        self.assertEqual(cents_to_eur(15000), 15)
        self.assertLess(cents_to_eur(15000), 15000)

    def test_word_to_number(self):
        self.assertEqual(text_to_number('fifteen'), 15)
        self.assertIsInstance(text_to_number('ten'), int)

    def tearDown(self):
        del self.test_path
        del self.na


if __name__ == '__main__':
    unittest.main()
