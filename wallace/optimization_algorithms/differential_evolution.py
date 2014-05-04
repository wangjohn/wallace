import random

from wallace.optimization_algorithms.optimization_algorithm import OptimizationAlgorithm, OptimizationAlgorithmModelWrapper
from wallace.weighted_selection import WeightedSelection
from wallace.parameters import ParameterSet
from wallace.independent_variables import IndependentVariableSelection

class DifferentialEvolution(OptimizationAlgorithm):
    def __init__(self, dataset, dependent_variable, settings, predictive_model_generator):
        OptimizationAlgorithm.__init__(self, dataset, dependent_variable, settings, predictive_model_generator)

    def update_population(self):
        updated_population = []
        for target_wrapper in self.model_population:
            target_model = target_wrapper.model
            parameter_selection = DEParameterSelection(self.settings, target_wrapper, self.model_population, self.full_validity_check)
            parameter_set = parameter_selection.generate_parameter_set()

            independent_variable_selection = target_wrapper.independent_variable_selection
            de_variable_selection = DEIndependentVariableSelection(self.settings, target_wrapper, self.model_population, self.dataset)
            independent_variables = de_variable_selection.generate_independent_variables()

            model_information = self.predictive_model_generator.choose_model_type()
            model_class = model_information["model_class"]

            updated_model = model_class(self.settings, parameter_set, self.dependent_variable, independent_variables)

            if self.evaluate_fitness(updated_model) <= self.evaluate_fitness(target_model):
                independent_variable_selection.increase_probabilities(independent_variables)
                updated_wrapper = OptimizationAlgorithmModelWrapper(updated_model, independent_variable_selection)
            else:
                updated_wrapper = OptimizationAlgorithmModelWrapper(target_model, independent_variable_selection)

            updated_population.append(updated_wrapper)

        self.model_population = updated_population

class DEIndependentVariableSelection(object):
    def __init__(self, settings, target_wrapper, model_population, dataset):
        self.settings = settings
        self.target_wrapper = target_wrapper
        self.model_population = self.model_population
        self.dataset = dataset

    def generate_independent_variables(self):
        de_selection = DESelection(self.settings)
        wrappers = de_selection.generate_distinct(self.target_wrapper, self.model_population, 3)
        independent_variable_selections = [wrapper.independent_variable_selection for wrapper in wrappers]
        probability_hashes = [selection.get_probabilities() for selection in independent_variable_selections]

        independent_variables = []
        for independent_variable in self.dataset.get_independent_variables():
            probabilities = [probability_container[independent_variable] for probability_hash in probability_hashes]
            variable_probability = de_selection.mutate(*probabilities)
            if random.random() < variable_probability:
                independent_variables.append(independent_variable)
        return independent_variables

class DESelection(object):
    def __init__(self, settings):
        self.settings = settings

    def generate_distinct(self, target, population, num_distinct=3):
        population = list(population)
        population.remove(target)
        return random.sample(population, num_distinct)

    def mutate(self, param1, param2, param3):
        rand = random.random()
        if rand < self.crossover_probability():
            return param1 + self.differential_weight()*(param2 - param3)

    def crossover_probability(self):
        return self.settings.get("differential_evolution.crossover_probability")

    def differential_weight(self):
        return self.settings.get("differential_evolution.differential_weight")

class DEParameterSelection(object):
    def __init__(self, settings, target_wrapper, model_population, validity_check):
        self.settings = settings
        self.target_wrapper = target_wrapper
        self.model_population = model_population
        self.validity_check = validity_check

    def generate_parameter_set(self):
        de_selection = DESelection(self.settings)
        selected_wrappers = de_selection.generate_distinct(self.target_wrapper, self.model_population, 3)
        parameter_values = {}
        for parameter_name in self.validity_check.list_parameter_names():
            parameter_type = self.validity_check.get_parameter_type(parameter_name)
            if parameter_type == "CategoryParameter" or parameter_type == "IntegerRangeParameter":
                updated_value = self.validity_check.get_valid_value(parameter_name)
            else:
                selected_parameters = [wrapper.model.parameter_set.get(parameter_name) for wrapper in selected_wrappers]
                updated_value = de_selection.mutate(*selected_parameters)

                if updated_value == None:
                    updated_value = self.target_wrapper.model.parameter_set.get(parameter_name)
                elif not self.validity_check.check_validity(parameter_name, updated_value).is_valid:
                    updated_value = self.validity_check.get_valid_value(parameter_name)

            parameter_values[parameter_name] = updated_value
        return ParameterSet(parameter_values, validity_check=self.validity_check)
