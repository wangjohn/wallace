import random

from wallace.predictive_models.predictive_model import PredictiveModel
from wallace.parameters import ParameterSet
from wallace.weighted_selection import WeightedSelection

class PredictiveModelGenerator(object):
    def __init__(self, settings, default_validity_check=None):
        self.settings = settings
        self.model_types = {}
        self.default_validity_check = default_validity_check

    def add_model_type(self, model_klass, parameter_validity_check=None, weight=None):
        if not issubclass(model_klass, PredictiveModel):
            raise ValueError("Model types added to the model generator must be subclasses of PredictiveModel.")
        if model_klass.__name__ not in self.model_types:
            if parameter_validity_check == None:
                parameter_validity_check = self.default_validity_check
            self.model_types[model_klass.__name__] = {
                "model_class": model_klass,
                "parameter_validity_check": parameter_validity_check,
                "weight": weight
                }

    def choose_model_type(self):
        weighted_selection = WeightedSelection()
        for model_name, information_hash in self.model_types.iteritems():
            weighted_selection.add_selection(model_name, information_hash["weight"])

        model_name = weighted_selection.choose()
        return self.model_types[model_name]

    def get_parameter_set_from_class(self, model_klass):
        model_name = model_klass.__name__
        return self.get_parameter_set(model_name)

    def get_parameter_set(self, model_name):
        if issubclass(model_name, PredictiveModel):
            model_name = model_name.__name__
        if model_name not in self.model_types:
            raise ValueError("Model '%s' is not a valid model type for this model generator." % model_name)

        model_information = self.model_types[model_name]
        validity_check = model_information["parameter_validity_check"]

        parameter_values = {}
        for parameter_name in model.required_parameters():
            value = validity_check.get_valid_value(parameter_name)
            parameter_values[parameter_name] = value

        return ParameterSet(parameter_values, validity_check=validity_check)
