from unittest import TestCase
import os

from wallace.settings import AbstractSettings
from wallace.dataset_file_reader import DatasetFileReader

class DatasetFileReaderTest(TestCase):
    def setUp(self):
        settings = AbstractSettings({})
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), './sample_dataset.csv'))
        self.dataset_file_reader = DatasetFileReader(settings, path)

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

    def test_greedy_read_lines_stops_correctly(self):
        input_rows = [[1,2,3],[2,2,3],[3,2,3],[4,2,3],[5,2,3]]
        data_matrix = self.dataset_file_reader.greedy_read_lines(input_rows, 3)

        self.assertEqual(3, len(data_matrix))
        self.assertListEqual([1,2,3], data_matrix[0])
        self.assertListEqual([2,2,3], data_matrix[1])
        self.assertListEqual([3,2,3], data_matrix[2])

    def test_randomized_read_lines_stops_correctly(self):
        input_rows = [[1,2,3],[2,2,3],[3,2,3],[4,2,3],[5,2,3]]
        data_matrix = self.dataset_file_reader.randomized_read_lines(input_rows, 3)

        self.assertEqual(3, len(data_matrix))

    def test_reading_csv_correctly(self):
        dataset = self.dataset_file_reader.read()

        self.assertEqual(0, dataset.column_index("header1"))
        self.assertEqual(1, dataset.column_index("header2"))
        self.assertEqual(2, dataset.column_index("header3"))
        self.assertEqual(3, dataset.column_index("header4"))

        with self.assertRaises(ValueError):
            dataset.column_index("some_header_that_doesn't_exist")

        self.assertListEqual([1252, 't', 'john', 'wang'], dataset.get_row(0))
        self.assertListEqual([1234, 'f', 'bob', 'hope'], dataset.get_row(1))
        self.assertListEqual([5555, 'f', 'rob', 'bernham'], dataset.get_row(2))
        self.assertListEqual([99, 't', 'paul', 'graham'], dataset.get_row(3))

        with self.assertRaises(IndexError):
            dataset.get_row(4)

