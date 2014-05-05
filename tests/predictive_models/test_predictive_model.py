from unittest import TestCase

from wallace.parameters import ParameterSet
from wallace.predictive_models.predictive_model import PredictiveModel
from wallace.dataset import DatasetVariable
from wallace.parameters import ParametersGeneralValidityCheck

class RequiredParametersPredictiveModel(PredictiveModel):
    @classmethod
    def validity_check(self):
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_range_parameter("param1", 0.0, 1.0)
        validity_check.set_range_parameter("param2", 0.0, 1.0)
        validity_check.set_range_parameter("param3", 0.0, 1.0)
        return validity_check

class PredictiveModelTest(TestCase):
    def test_required_parameters(self):
        dictionary = {
            "param1": {
                    "type": "range",
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "value": 0.5
                },
            "param2": {
                    "type": "range",
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "value": 0.5
                },
            "param3": {
                    "type": "range",
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "value": 0.5
                }
            }

        settings = {}
        parameter_set = ParameterSet.create_from_dict(dictionary)
        dependent_variable = DatasetVariable(0)
        independent_variables = [DatasetVariable(1)]

        RequiredParametersPredictiveModel(settings, parameter_set, dependent_variable, independent_variables)

    def test_missing_required_parameters_raises_error(self):
        dictionary = {
            "param1": {
                    "type": "range",
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "value": 0.5
                },
            "param3": {
                    "type": "range",
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "value": 0.5
                }
            }

        settings = {}
        parameter_set = ParameterSet.create_from_dict(dictionary)
        dependent_variable = DatasetVariable(0)
        independent_variables = [DatasetVariable(1)]

        with self.assertRaises(AssertionError):
            RequiredParametersPredictiveModel(settings, parameter_set, dependent_variable, independent_variables)
