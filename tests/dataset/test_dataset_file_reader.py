from unittest import TestCase

from wallace.settings import AbstractSettings
from wallace.dataset_file_reader import DatasetFileReader

class DatasetFileReaderTest(TestCase):
    def setUp(self):
        settings = AbstractSettings({})
        self.dataset_file_reader = DatasetFileReader(settings, "filename")

    def test_detect_headers_for_representative_dataset(self):
        actual_headers = ["header0", "header1", "header2"]
        data_matrix = [actual_headers,
                ["some_string", 1, "t"],
                ["another_str", 10, "f"]]
        result_matrix, headers = self.dataset_file_reader.detect_headers(data_matrix)

        self.assertEqual(2, len(result_matrix))
        self.assertListEqual(actual_headers, headers)

    def test_detect_headers_when_there_are_booleans_in_dataset(self):
        actual_headers = ["header0", "t", "header2"]
        data_matrix = [actual_headers,
                ["some_string", "t", "t"],
                ["another_str", "t", "f"]]
        result_matrix, headers = self.dataset_file_reader.detect_headers(data_matrix)

        self.assertEqual(2, len(result_matrix))
        self.assertListEqual(actual_headers, headers)

    def test_detects_no_headers_for_headerless_datasets(self):
        data_matrix = [[145, "john", "wang"],
                [534, "bob", "hope"],
                [1, "david", "hansson"]]

        result_matrix, headers = self.dataset_file_reader.detect_headers(data_matrix)

        self.assertEqual(3, len(result_matrix))
        self.assertEqual(None, headers)

    def test_parsing_data_types_correctly_for_strings(self):
        row = ["some string", "2string", "string24531234 34534 345", "2.345s"]
        data_types = self.dataset_file_reader.parse_data_types(row)
        self.assertEqual(str, data_types[0])
        self.assertEqual(str, data_types[1])
        self.assertEqual(str, data_types[2])
        self.assertEqual(str, data_types[3])

    def test_parsing_data_types_correctly_for_ints_and_floats(self):
        row = ["1234", "  34.231 ", " 32. 43 ", " 5399999999999999 ", "23452345234523452345245.24"]
        data_types = self.dataset_file_reader.parse_data_types(row)
        self.assertEqual(int, data_types[0])
        self.assertEqual(float, data_types[1])
        self.assertEqual(str, data_types[2])
        self.assertEqual(int, data_types[3])
        self.assertEqual(float, data_types[4])

    def test_parsing_data_types_correclty_for_bools(self):
        row = ["t", "true", "True", "TRUE", "f", "false", "False", "FALSE"]
        data_types = self.dataset_file_reader.parse_data_types(row)
        self.assertEqual(bool, data_types[0])
        self.assertEqual(bool, data_types[1])
        self.assertEqual(bool, data_types[2])
        self.assertEqual(bool, data_types[3])
        self.assertEqual(bool, data_types[4])
        self.assertEqual(bool, data_types[5])
        self.assertEqual(bool, data_types[6])
        self.assertEqual(bool, data_types[7])
