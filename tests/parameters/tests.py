from unittest import TestCase

from wallace import parameters

class ParameterSetTest(TestCase):
    def test_single_range_dictionary(self):
        dictionary = {
            "my_parameter": {
                "type": "range",
                "lower_bound": 0.2,
                "upper_bound": 0.6,
                "value": 0.4
                }
            }
        parameter_set = parameters.ParameterSet.create_from_dict(dictionary)
        self.assertEqual(0.4, parameter_set.get("my_parameter"))

        parameter_set.set("my_parameter", 0.35)
        self.assertEqual(0.35, parameter_set.get("my_parameter"))

        with self.assertRaises(ValueError):
            parameter_set.set("my_parameter", 0.1)

        with self.assertRaises(ValueError):
            parameter_set.set("my_parameter", 0.8)

    def test_single_integer_range_dictionary(self):
        dictionary = {
            "my_parameter": {
                "type": "integer_range",
                "lower_bound": 10,
                "upper_bound": 25,
                "value": 15
                }
            }
        parameter_set = parameters.ParameterSet.create_from_dict(dictionary)
        self.assertEqual(15, parameter_set.get("my_parameter"))

        parameter_set.set("my_parameter", 18)
        self.assertEqual(18, parameter_set.get("my_parameter"))

        with self.assertRaises(ValueError):
            parameter_set.set("my_parameter", 15.12)

        with self.assertRaises(ValueError):
            parameter_set.set("my_parameter", 1)

        with self.assertRaises(ValueError):
            parameter_set.set("my_parameter", 28)

    def test_single_category_dictionary_no_weights(self):
        dictionary = {
            "my_parameter": {
                "type": "category",
                "categories": [True, False],
                "value": True
                }
            }
        parameter_set = parameters.ParameterSet.create_from_dict(dictionary)
        self.assertEqual(True, parameter_set.get("my_parameter"))

        parameter_set.set("my_parameter", False)
        self.assertEqual(False, parameter_set.get("my_parameter"))

        with self.assertRaises(ValueError):
            parameter_set.set("my_parameter", "some string")

        with self.assertRaises(ValueError):
            parameter_set.set("my_parameter", 1234)
