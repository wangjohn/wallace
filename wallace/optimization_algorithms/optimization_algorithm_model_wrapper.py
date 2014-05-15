import json

class OptimizationAlgorithmModelWrapper(object):
    def __init__(self, model, independent_variable_selection, fitness=None):
        self.model = model
        self.independent_variable_selection = independent_variable_selection
        self.fitness = fitness

    def json(self):
        return json.dumps(self.dictionary())

    def dictionary(self):
        return {
            "fitness": self.fitness,
            "model_name": self.model.model_name(),
            "independent_variables": [var.variable for var in self.model.independent_variables],
            "dependent_variable": self.model.dependent_variable.variable,
            "parameter_set": self.model.get_parameters()
            }

