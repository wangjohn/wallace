from unittest import TestCase
from datetime import datetime

from wallace.dataset_cleaner import DatasetCleaner
from wallace.settings import AbstractSettings
from wallace.data_type import DataType

class DatasetCleanerTest(TestCase):
    def setUp(self):
        self.settings = AbstractSettings({
                "dataset.remove_rows_with_missing_data": True,
                "dataset.maximum_missing_data_percentage": 1.0
            })
        self.data_matrix = [
                ["3421", "1232", "hello", "t", "5/12/2003"],
                ["2123", "2221", "mello", "f", "3/12/1995"],
                ["5234", "", "treble", "f", "5/5/2013"],
                ["NaN", "NaN", "bobble", "t", "3/1/2004"]
                ]

        self.dataset_cleaner = DatasetCleaner(self.settings, self.data_matrix)

    def test_clean_entry_on_missing_data_raises_exception(self):
        self.assertEqual(None, self.dataset_cleaner.clean_entry("NaN", DataType("string")))
        self.assertEqual(None, self.dataset_cleaner.clean_entry("", DataType("float")))
        self.assertEqual(None, self.dataset_cleaner.clean_entry("NA", DataType("integer")))

    def test_clean_entry_on_date(self):
        cleaned_entry = self.dataset_cleaner.clean_entry("4/25/2013", DataType("date"))
        timestamp = (datetime(2013, 4, 25) - datetime(1970, 1, 1)).total_seconds()
        self.assertEqual(timestamp, cleaned_entry)

    def test_fully_cleaning_the_dataset(self):
        cleaned_matrix = self.dataset_cleaner.clean()

        timestamp1 = (datetime(2003, 5, 12) - datetime(1970, 1, 1)).total_seconds()
        timestamp2 = (datetime(1995, 3, 12) - datetime(1970, 1, 1)).total_seconds()
        self.assertEqual(2, len(cleaned_matrix))
        self.assertListEqual([3421, 1232, "hello", "t", timestamp1], cleaned_matrix[0])
        self.assertListEqual([2123, 2221, "mello", "f", timestamp2], cleaned_matrix[1])

    def test_incorrect_number_of_columns_raises_exception(self):
        matrix = list(self.data_matrix)
        matrix.append(["NaN", "NaN", "string"])
        dataset_cleaner = DatasetCleaner(self.settings, matrix)

        with self.assertRaises(ValueError):
            dataset_cleaner.clean()

    def test_cleaning_sparse_columns(self):
        settings = AbstractSettings({
                "dataset.remove_rows_with_missing_data": True,
                "dataset.maximum_missing_data_percentage": 0.25
            })
        non_sparse_data_matrix = [
                ["13", "123"],
                ["23", "234"],
                ["34", "455"],
                ["12", "345"],
                ["11", "235"],
                ["34", "234"],
                [None, "234"]
                ]
        sparse_data_matrix = [
                [None, "324"],
                [None, "232"],
                [None, "123"],
                [None, "234"],
                [None, "234"],
                ["1111", "234"],
                ["4324", None],
                ]
        non_sparse_dataset_cleaner = DatasetCleaner(settings, non_sparse_data_matrix)
        sparse_dataset_cleaner = DatasetCleaner(settings, sparse_data_matrix)

        matrix = non_sparse_dataset_cleaner.clean()
        self.assertEqual(6, len(matrix))
        self.assertListEqual([13, 123], matrix[0])
        self.assertListEqual([23, 234], matrix[1])
        self.assertListEqual([34, 455], matrix[2])
        self.assertListEqual([12, 345], matrix[3])
        self.assertListEqual([11, 235], matrix[4])
        self.assertListEqual([34, 234], matrix[5])

        matrix = sparse_dataset_cleaner.clean()
        self.assertEqual(6, len(matrix))
        self.assertListEqual([None, 324], matrix[0])
        self.assertListEqual([None, 232], matrix[1])
        self.assertListEqual([None, 123], matrix[2])
        self.assertListEqual([None, 234], matrix[3])
        self.assertListEqual([None, 234], matrix[4])
        self.assertListEqual([1111, 234], matrix[5])
