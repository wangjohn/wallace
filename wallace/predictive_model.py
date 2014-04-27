import random

class PredictiveModel(object):
    def __init__(self, parameters_set=None):
        self.set_parameters(parameters_set)
        self.independent_variables = []

    def independent_variables(self):
        return self.independent_variables

    def predict(self, input_data):
        raise NotImplementedError()

    def set_parameters(self, parameters_set):
        self.parameters_set = parameters_set
