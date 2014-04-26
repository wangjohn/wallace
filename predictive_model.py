import random

class PredictiveModel(object):
    def __init__(self, parameters=None):
        self.set_parameters(parameters)
        self.independent_variables = []

    def independent_variables(self):
        return self.independent_variables

    def predict(self, data):
        raise NotImplementedError()

    def set_parameters(self, parameters):
        self.parameters = parameters

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

class ParametersRangeValidityCheck(ParametersValidityCheck):
    def __init__(self, ranges=None):
        if ranges == None:
            self.ranges = {}
        else:
            self.ranges = ranges

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

class ParametersValidityCheckResult(object):
    def __init__(self, is_valid, message=None):
        self.is_valid = is_valid
        self.message = message
