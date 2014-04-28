import random

from wallace.predictive_models import PredictiveModel
from wallace.parameters import ParameterSet

class PredictiveModelGenerator(object):
    def __init__(self, settings):
        self.settings = settings
        self.model_types = {}

    def add_model_type(self, model_klass, parameter_validity_check, weight=None):
        if not issubclass(model_klass, PredictiveModel):
            raise ValueError("Model types added to the model generator must be subclasses of PredictiveModel.")
        if model_klass not in self.models:
            self.models[model_klass.__name__] = {
                "model_class": model_klass,
                "parameter_validity_check": parameter_validity_check,
                "weight": weight
                }

    def choose_model_type(self):
        normalized_weights = self._normalize_weights()
        if normalized_weights == None:
            model_name = random.choice(self.model_types.keys())
            return self.model_types[model_name]
        else:
            rand = random.random()
            current_sum = 0
            for model_name, weight in normalized_weights.iteritems():
                if rand <= weight + current_sum:
                    return self.model_types[model_name]
                current_sum += weight

    def get_parameter_set_from_class(self, model_klass):
        model_name = model_klass.__name__
        return self.get_parameter_set(model_name)

    def get_parameter_set(self, model_name):
        if model_name not in self.model_types:
            raise ValueError("Model '%s' is not a valid model type for this model generator." % model_name)

        model_information = self.model_types[model_name]
        validity_check = model_information["parameter_validity_check"]

        parameter_values = {}
        for parameter_name in validity_check.list_parameter_names():
            value = validity_check.get_valid_value(parameter_name)
            parameter_values[parameter_name] = value

        return ParameterSet(parameter_values, validity_check=validity_check)

    def _normalize_weights(self):
        non_weighted = 0
        total_weight = 0
        for information_hash in self.model_types.itervalues():
            if "weight" in information_hash:
                total_weight += information_hash["weight"]
            else:
                non_weighted += 1

        if non_weighted == len(self.model_types):
            return None

        average_weight = float(total_weight) / (len(self.model_types) - non_weighted)
        total_weight += average_weight * non_weighted

        normalized_weights = {}
        for model_name, information_hash in self.model_types.iteritems():
            if "weight" in information_hash:
                normalized_weight = float(information_hash["weight"]) / total_weight
            else:
                normalized_weight = average_weight
            normalized_weights[model_name] = normalized_weight

        return normalized_weights

