import random

class PredictiveModel(object):
    def __init__(self, settings, parameter_set, dependent_variable, independent_variables):
        self.parameter_set = parameter_set
        self.settings = settings
        self.dependent_variable = dependent_variable
        self.independent_variables = []

    def independent_variables(self):
        return self.independent_variables

    def dependent_variable(self):
        return self.dependent_variable

    def train(self, dataset):
        raise NotImplementedError()

class PredictiveModelVariable(object):
    def __init__(self, variable):
        self.variable = variable

    def get_column_index(self, dataset):
        if isinstance(self.variable, int):
            if 0 <= self.variable and self.variable < dataset.num_cols:
                return self.variable
            else:
                raise ValueError("Variable is out of the range of the dataset.")
        else:
            return self.dataset.column_index(self.variable)

class TrainedPredictiveModel(object):
    def __init__(self, settings, predictive_model, dataset):
        self.settings = settings
        self.predictive_model = predictive_model
        self.dataset = dataset

    def predict(self, dataset):
        raise NotImplementedError()

    def predict_and_evaluate_fitness(self, dataset):
        raise NotImplementedError()
