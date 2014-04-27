import random

class PredictiveModel(object):
    def __init__(self, settings, parameter_set):
        self.parameter_set = parameter_set
        self.settings = settings
        self.independent_variables = []

    def independent_variables(self):
        return self.independent_variables

    def predict(self, input_data):
        raise NotImplementedError()

    def evaluate_fitness(self, dataset):
        raise NotImplementedError()
