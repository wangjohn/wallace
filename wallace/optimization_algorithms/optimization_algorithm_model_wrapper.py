import json

class OptimizationAlgorithmModelWrapper(object):
    def __init__(self, model, independent_variable_selection, fitness=None):
        self.model = model
        self.independent_variable_selection = independent_variable_selection
        self.fitness = fitness

    def get_parameters(self):
        params = {}
        for parameter_name in self.model.parameter_set.validity_check.list_parameter_names():
            params[name] = self.model.parameter_set.get(parameter_name)

        return params

    def json(self):
        dictionary = {
            "fitness": self.fitness,
            "independent_variables": [var.variable for var in self.model.independent_variables],
            "dependent_variable": self.model.dependent_variable.var,
            "parameter_set": self.get_parameters()
            }
        return json.dumps(dictionary)
