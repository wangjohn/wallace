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
