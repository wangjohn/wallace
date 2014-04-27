from unittest import TestCase

from wallace import parameters

class ParameterSetTest(TestCase):
    def test_single_parameter_dictionary(self):
        dictionary = {
            "my_parameter": {
                "type": "range",
                "lower_bound": 0.2,
                "upper_bound": 0.6,
                "value": 0.4
                }
            }
        parameter_set = parameters.ParameterSet.create_from_dict(dictionary)
        self.assertEqual(parameter_set.get("my_parameter"), 0.4)

