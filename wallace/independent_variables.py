import random

from wallace.weighted_selection import WeightedSelection
from wallace.dataset import DatasetVariable

class IndependentVariableSelection(object):
    def __init__(self, settings, dependent_variable, potential_independent_variables):
        self.settings = settings
        self.dependent_variable = dependent_variable
        self.potential_independent_variables = potential_independent_variables
        self.selection_probabilities = self._initialize_selection_probabilities(self.potential_independent_variables)
        self.variable_count_probabilities = self._initialize_variable_count_probabilities(self.potential_independent_variables)

    def _initialize_selection_probabilities(self, potential_independent_variables):
        selections = {}
        for variable in potential_independent_variables:
            selections[variable.variable] = None
        return WeightedSelection(selections)

    def _initialize_variable_count_probabilities(self, potential_independent_variables):
        selections = {}
        for i in xrange(1, len(potential_independent_variables)):
            selections[i] = None
        return WeightedSelection(selections)

    def initialize_independent_variables(self, num_variables=None):
        if num_variables == None:
            percentage = self.settings.get("independent_variable_selection.initial_independent_variables_percentage")
            num_variables = int(len(self.potential_independent_variables)*percentage)

        return random.sample(self.potential_independent_variables, num_variables)

    def select_independent_variables(self, probabilities=None):
        num_variables = self.variable_count_probabilities.choose()
        if probabilities == None:
            probabilities = self.selection_probabilities

        return WeightedSelection.sample(probabilities, num_variables)

    def get_probability(self, variable):
        selection = self._get_selection(variable)
        return self.selection_probabilities.get_probability(selection)

    def get_variable_count_probability(self, num_variables):
        if self.variable_count_probabilities.contains(num_variables):
            return self.variable_count_probabilities.get_probability(num_variables)
        else:
            return 0

    def increase_probability(self, variable):
        selection = self._get_selection(variable)
        self.selection_probabilities.increase_weight(selection)

    def increase_variable_count_probability(self, num_variables):
        self.variable_count_probabilities.increase_weight(num_variables)

    def increase_probabilities(self, variables):
        self.increase_variable_count_probability(len(variables))
        for variable in variables:
            self.increase_probability(variable)

    def _get_selection(self, variable):
        if isinstance(variable, DatasetVariable):
            return variable.variable
        else:
            return variable
