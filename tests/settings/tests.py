from unittest import TestCase

from wallace import settings
from .fixtures import *

class SettingsTest(TestCase):
    def test_default_abstract_settings(self):
        settings_object = settings.AbstractSettings()

        self.assertEqual(1, settings_object.get("setting_1"))
        self.assertEqual(2, settings_object.get("setting_2"))
        self.assertEqual(3, settings_object.get("setting_3"))

    def test_default_settings_get_overridden(self):
        new_settings = {
            "setting_1": 5,
            "setting_4": 10
            }
        settings_object = settings.AbstractSettings(new_settings)

        self.assertEqual(5, settings_object.get("setting_1"))
        self.assertEqual(2, settings_object.get("setting_2"))
        self.assertEqual(3, settings_object.get("setting_3"))
        self.assertEqual(10, settings_object.get("setting_4"))

    def test_setting_a_function(self):
        new_settings = {
            "setting_1": lambda : 15,
            "setting_2": lambda x : x
            }
        settings_object = settings.AbstractSettings(new_settings)

        self.assertEqual(15, settings_object.get("setting_1"))
        self.assertEqual(10, settings_object.get("setting_2", 10))
        self.assertEqual(20, settings_object.get("setting_2", 20))
        self.assertEqual(3, settings_object.get("setting_3"))

    def test_setting_a_function_with_multiple_arguments(self):
        new_settings = {
            "setting_1": lambda x, y, z : x + y + z
            }
        settings_object = settings.AbstractSettings(new_settings)

        self.assertEqual(3, settings_object.get("setting_1", 0, 1, 2))
        self.assertEqual(60, settings_object.get("setting_1", 15, 20, 25))
        self.assertEqual(2, settings_object.get("setting_2"))
        self.assertEqual(3, settings_object.get("setting_3"))

    def test_setting_attribute_after_settings_object_has_been_created(self):
        settings_object = settings.AbstractSettings()
        settings_object.set("something.whatever", "something")

        self.assertEqual("something", settings_object.get("something.whatever"))
