from unittest import TestCase

from wallace.interval_storage import IntervalStorage
from wallace.settings import AbstractSettings

class IntervalStorageTest(TestCase):
    def test_interval_storage_with_a_single_interval(self):
        interval_storage = IntervalStorage()
        self.assertFalse(interval_storage.has_intersection(0.0, 1.0))
        interval_storage.add_interval("1", 0.0, 1.0)

        self.assertEqual("1", interval_storage.get_entry(0.5))

        with self.assertRaises(ValueError):
            interval_storage.get_entry(1.5)

    def test_interval_storage_for_invalid_intervals(self):
        interval_storage = IntervalStorage()
        with self.assertRaises(ValueError):
            interval_storage.add_interval("1", 0.0, 1.2)

        with self.assertRaises(ValueError):
            interval_storage.add_interval("1", -3.2, 0.8)

        with self.assertRaises(ValueError):
            interval_storage.add_interval("1", -3.2, 1.4)

    def test_interval_storage_with_two_intervals_and_midpoint_get(self):
        interval_storage = IntervalStorage()
        interval_storage.add_interval("1", 0.0, 0.5)
        interval_storage.add_interval("2", 0.5, 1.0)

        self.assertEqual("1", interval_storage.get_entry(0.25))
        self.assertEqual("2", interval_storage.get_entry(0.5))
        self.assertEqual("2", interval_storage.get_entry(0.8))

