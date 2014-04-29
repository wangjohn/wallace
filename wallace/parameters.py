import random
import copy

class ParameterSet(object):
    def __init__(self, parameter_values, validity_check=None, default_values=None):
        self.parameter_values = parameter_values
        self.validity_check = validity_check
        if default_values == None:
            self.default_values = {}
        else:
            self.default_values = default_values

    def get(self, parameter_name):
        result = self._get(parameter_name)
        if result == None:
            raise KeyError("Parameter '%s' was not defined" % parameter_name)
        else:
            return result

    def has_parameter(self, parameter_name):
        return self._get(parameter_name) != None

    def get_valid_value(self, parameter_name):
        if self.validity_check == None:
            raise ValueError("Cannot get valid value without a validity check.")
        else:
            return self.validity_check.get_valid_value(parameter_name)

    def set(self, parameter_name, value):
        if self.validity_check == None:
            self.parameter_values[parameter_name] = value
        else:
            validity_result = self.validity_check.check_validity(parameter_name, value)
            if validity_result.is_valid:
                self.parameter_values[parameter_name] = value
            else:
                raise ValueError("Parameter assignment did not pass validity check: %s" % validity_result.message)

    def copy(self):
        """
        Returns a semi-deep copy of a ParameterSet. The parameter values will have
        a deep copy, but the validity_check and default_values attributes will be
        shared across all copies.
        """
        parameter_values = copy.deepcopy(self.parameter_values)
        return ParameterSet(parameter_values, self.validity_check, self.default_values)

    @classmethod
    def create_from_dict(klass, dictionary):
        """
        Takes a dictionary and converts it into a ParameterSet. Dictionaries
        should be of the following form:

        dictionary = {
            "range_parameter_name": {
                "type": "range",
                "lower_bound": 0.0,
                "upper_bound": 1.0,
                "value": 0.3423, # optional
                "default": 0.5, # optional
            },
            "integer_range_parameter_name": {
                "type": "integer_range",
                "lower_bound": 123,
                "upper_bound": 156,
                "value": 133, # optional
                "default": 150, # optional
            },
            "category_parameter_name": {
                "type": "category",
                "categories": [True, False],
                "weights": [0.3, 0.6], # optional
                "value": True, # optional
                "default": True, # optional
            }
        }

        Currently supporting three types of parameters: range, integer_range,
        and category.
        """
        parameter_values = {}
        default_values = {}
        validity_check = ParametersGeneralValidityCheck()
        for parameter_name, param_options in dictionary.iteritems():
            if "value" in param_options:
                parameter_values[parameter_name] = param_options["value"]
            if "default" in param_options:
                default_values[parameter_name] = param_options["default"]

            _initialize_validity_check(parameter_name, param_options, validity_check)

        return klass(parameter_values, validity_check, default_values)

    def _get(self, parameter_name):
        if parameter_name in self.parameter_values:
            return self.parameter_values[parameter_name]
        if parameter_name in self.default_values:
            return self.default_values[parameter_name]


def _initialize_validity_check(parameter_name, param_options, validity_check):
    param_type = _get_param_option(param_options, "type", True, parameter_name)
    if param_type == "range":
        lower_bound = _get_param_option(param_options, "lower_bound", True, parameter_name)
        upper_bound = _get_param_option(param_options, "upper_bound", True, parameter_name)
        validity_check.set_range_parameter(parameter_name, lower_bound, upper_bound)
    elif param_type == "integer_range":
        lower_bound = _get_param_option(param_options, "lower_bound", True, parameter_name)
        upper_bound = _get_param_option(param_options, "upper_bound", True, parameter_name)
        validity_check.set_integer_range_parameter(parameter_name, lower_bound, upper_bound)
    elif param_type == "category":
        categories = _get_param_option(param_options, "categories", True, parameter_name)
        weights = _get_param_option(param_options, "categories")
        validity_check.set_category_parameter(parameter_name, categories, weights)
    else:
        raise ValueError("Malformed dictionary for parameter '%s': '%s' is not a valid parameter type" % \
                (parameter_name, param_type))

def _get_param_option(param_options, param_option_name, required=False, parameter_name=None):
    if param_option_name in param_options:
        return param_options[param_option_name]
    elif required:
        raise ValueError("Malformed dictionary for parameter '%s': required parameter '%s' does not exist" % \
                (parameter_name, param_option_name))

class ParametersValidityCheck(object):
    def check_validity(self, parameter_name, value):
        return ParametersValidityCheckResult(True, "")

    def get_valid_value(self, parameter_name):
        raise NotImplementedError()

class ParametersGeneralValidityCheck(ParametersValidityCheck):
    def __init__(self, parameters=None):
        if parameters == None:
            self.parameters = {}
        else:
            self.parameters = parameters

    def set_range_parameter(self, parameter_name, lower_bound, upper_bound):
        self.parameters[parameter_name] = RangeParameter(lower_bound, upper_bound)

    def set_integer_range_parameter(self, parameter_name, lower_bound, upper_bound):
        self.parameters[parameter_name] = IntegerRangeParameter(lower_bound, upper_bound)

    def set_category_parameter(self, parameter_name, categories, weights=None):
        self.parameters[parameter_name] = CategoryParameter(categories, weights)

    def set_parameter(self, parameter_name, parameter):
        if isinstance(parameter, BasicParameter):
            self.parameters[parameter_name] = parameter
        else:
            raise TypeError("Parameters must be subclasses of BasicParameter.")

    def list_parameter_names(self):
        return self.parameters.keys()

    def check_validity(self, parameter_name, value):
        self._check_parameter_existence(parameter_name)
        return self.parameters[parameter_name].check_validity(value)

    def get_valid_value(self, parameter_name):
        self._check_parameter_existence(parameter_name)
        return self.parameters[parameter_name].get_valid_value()

    def _check_parameter_existence(self, parameter_name):
        if parameter_name not in self.parameters:
            raise ValueError("Parameter '%s' does not have a validity check defined." % parameter_name)

class BasicParameter(object):
    def __init__(self, parameter_type, value=None):
        self.parameter_type = parameter_type
        self.value = value

    def get_valid_value(self, data=None):
        raise NotImplementedError("This method should be implemented by subclasses of BasicParameter.")

    def check_validity(self, value):
        raise NotImplementedError("This method should be implemented by subclasses of BasicParameter.")

class RangeParameter(BasicParameter):
    def __init__(self, lower_bound, upper_bound):
        BasicParameter.__init__(self, "range")
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_valid_value(self, data=None):
        return random.uniform(lower_bound, upper_bound)

    def check_validity(self, value):
        if self.lower_bound <= value and value <= self.upper_bound:
            return ParametersValidityCheckResult(True)
        else:
            message = ("Value '%s' is out of parameter range: [%s, %s]" % \
                    (value, self.lower_bound, self.upper_bound))
            return ParametersValidityCheckResult(False, message)

class IntegerRangeParameter(BasicParameter):
    def __init__(self, lower_bound, upper_bound):
        BasicParameter.__init__(self, "range")
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self._check_initialization()

    def get_valid_value(self, data=None):
        return random.randrange(lower_bound, upper_bound)

    def check_validity(self, value):
        if not isinstance(value, int):
            message = "Value '%s' is not an integer"
            return ParametersValidityCheckResult(False, message)
        if self.lower_bound <= value and value <= self.upper_bound:
            return ParametersValidityCheckResult(True)
        else:
            message = "Value '%s' is out of parameter range: [%s, %s]" % \
                    (value, self.lower_bound, self.upper_bound)
            return ParametersValidityCheckResult(False, message)

    def _check_initialization(self):
        if not (isinstance(self.lower_bound, int) and isinstance(self.upper_bound, int)):
            raise ValueError("Lower and upper bounds for IntegerRangeParameter must be integers")

class CategoryParameter(BasicParameter):
    def __init__(self, categories, weights = None):
        BasicParameter.__init__(self, "category")
        self.categories = categories
        self.weights = self._normalize_weights(weights)
        self._validate_weights(self.categories, self.weights)

    def check_validity(self, value):
        if value in self.categories:
            return ParametersValidityCheckResult(True)
        else:
            message = "Value '%s' is not a category" % value
            return ParametersValidityCheckResult(False, message)

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
