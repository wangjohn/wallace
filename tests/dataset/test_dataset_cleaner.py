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

    def test_clean_entry_on_row(self):
        cleaned_row = self.dataset_cleaner.clean_row(["1", "4/25/2013", "Bob"], [DataType("integer"), DataType("date"), DataType("string")])
        timestamp = (datetime(2013, 4, 25) - datetime(1970, 1, 1)).total_seconds()

        self.assertEqual(1, cleaned_row[0])
        self.assertEqual(timestamp, cleaned_row[1])
        self.assertEqual("Bob", cleaned_row[2])

    def test_clean_entry_on_row_raises_exception_for_missing_data(self):
        cleaned_row = self.dataset_cleaner.clean_row(["NaN", "4/25/2013", "Bob"], [DataType("integer"), DataType("date"), DataType("string")])
        timestamp = (datetime(2013, 4, 25) - datetime(1970, 1, 1)).total_seconds()
        self.assertEqual(None, cleaned_row[0])
        self.assertEqual(timestamp, cleaned_row[1])
        self.assertEqual("Bob", cleaned_row[2])

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
