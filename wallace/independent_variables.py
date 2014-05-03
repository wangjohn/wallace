import random

from wallace.weighted_selection import WeightedSelection
from wallace.dataset import DatasetVariable

class IndependentVariableSelection(object):
    def __init__(self, settings, dataset, dependent_variable):
        self.settings = settings
        self.dataset = dataset
        self.dependent_variable = dependent_variable
        self.independent_variables = self.dataset.get_independent_variables(self.dependent_variable)
        self.selection_probabilities = self._initialize_selection_probabilities(self.independent_variables)

    def _initialize_selection_probabilities(self, independent_variables):
        selections = {}
        for variable in independent_variables:
            selections[variable.variable] = None
        return WeightedSelection(selections)

    def initialize_independent_variables(self, num_variables=None):
        if num_variables == None:
            percentage = self.settings.get("independent_variable_selection.initial_independent_variables_percentage")
            num_variables = int(len(self.independent_variables)*percentage)

        return random.sample(self.independent_variables, num_variables)

    def get_probability(self, variable):
        selection = self._get_selection(variable)
        return self.selection_probabilities.get_probability(selection)

    def get_probabilities(self):
        probabilities = {}
        for independent_variable in self.independent_variables:
            probabilities[independent_variable] = self.get_probability(independent_variable)
        return probabilities

    def select_independent_variables(self):
        raise NotImplementedError()

    def increase_probability(self, variable):
        selection = self._get_selection(variable)
        self.selection_probabilities.increase_weight(selection)

    def increase_probabilities(self, variables):
        for variable in variables:
            self.increase_probability(variable)

    def _get_selection(self, variable):
        if isinstance(variable, DatasetVariable):
            return variable.variable
        else:
            return variable
