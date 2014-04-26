import random

class ParametersSet(object):
    def __init__(self, parameters, validity_check=None, defaults=None):
        self.parameters = parameters
        self.validity_check = validity_check
        if defaults == None:
            self.defaults = {}
        else:
            self.defaults = defaults

    def get(self, parameter_name):
        if parameter_name in self.parameters:
            return self.parameters[parameter_name]
        if parameter_name in self.defaults:
            return self.defaults[parameter_name]
        raise KeyError("Parameter '%s' was not defined" % parameter_name)

    def set(self, parameter_name, value):
        if self.validity_check != None:
            validity_result = self.validity_check.check_validity(parameter_name, value)
            if validity_result.is_valid:
                self.parameters[parameter_name] = value
            else:
                raise ValueError("Parameter assignment did not pass validity check: %s" % validity_result.message)
        else:
            self.parameters[parameter_name] = value

class ParametersValidityCheck(object):
    def check_validity(self, parameter_name, value):
        return ParametersValidityCheckResult(True, "")

    def get_valid_value(self, parameter_name):
        raise NotImplementedError()

# TODO: make this into a more general check. Something called GeneralParametersValidityCheck.
# This should handle:
#   1. Ranges (i.e. numbers)
#   2. Booleans
#   3. Categorical variables (might actually supersede booleans)
#
class ParametersRangeValidityCheck(ParametersValidityCheck):
    def __init__(self, parameters=None):
        if parameters == None:
            self.parameters = {}
        else:
            self.parameters = parameters

    def set_range(self, parameter_name, lower_bound, upper_bound):
        self.ranges[parameter_name] = (lower_bound, upper_bound)

    def check_validity(self, parameter_name, value):
        self._check_parameter_existence(parameter_name)
        (lower_bound, upper_bound) = self.ranges[parameter_name]
        if lower_bound <= value and value <= upper_bound:
            return ParametersValidityCheckResult(True)
        else:
            message = "Value '%s' is out of parameter range: [%s, %s]" %
                    (value, lower_bound, upper_bound)
            return ParametersValidityCheckResult(False, message)

    def get_valid_value(self, parameter_name):
        self._check_parameter_existence(parameter_name)
        (lower_bound, upper_bound) = self.ranges[parameter_name]
        return random.uniform(lower_bound, upper_bound)

    def _check_parameter_existence(self, parameter_name):
        if parameter_name not in self.ranges:
            raise ValueError("Parameter '%s' does not have a valid range of values defined." % parameter_name)

class BasicParameter(object):
    def __init__(self, parameter_type):
        self.parameter_type = parameter_type

    def get_valid_value(self, data=None):
        raise NotImplementedError("This method should be implemented by subclasses of BasicParameter.")

class RangeParameter(BasicParameter):
    def __init__(self, lower_bound, upper_bound):
        BasicParameter.__init__(self, "range")
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_valid_value(self, data=None):
        return random.uniform(lower_bound, upper_bound)

class CategoryParameter(BasicParameter):
    def __init__(self, categories, weights = None):
        BasicParameter.__init__(self, "category")
        self.categories = categories
        self.weights = self._normalize_weights(weights)
        self._validate_weights(self.categories, self.weights)

    def get_valid_value(self, data=None):
        if self.weights == None:
            return random.choice(self.categories)
        else:
            rand = random.random()
            current_sum = 0
            for i in xrange(len(self.categories)):
                if rand <= self.weights[i] + current_sum:
                    return self.categories[i]
                current_sum += self.weights[i]

            raise ArithmeticError("CategoryParameter's weights did not sum to 1")

    def _validate_weights(self, categories, weights):
        if weights != None and len(categories) != len(weights):
            raise ValueError("CategoryParameter's weights and categories are unequal lengths.")

    def _normalize_weights(self, weights):
        if weights == None:
            return None
        else:
            total_weight = sum(weights)
            normalized = []
            for weight in weights:
                normalized_weight = float(weight) / total_weight
                normalized.append(normalized_weight)
            return normalized


class ParametersValidityCheckResult(object):
    def __init__(self, is_valid, message=None):
        self.is_valid = is_valid
        self.message = message
