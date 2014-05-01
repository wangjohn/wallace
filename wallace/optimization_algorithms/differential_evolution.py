import random

from wallace.optimization_algorithms.optimization_algorithm import OptimizationAlgorithm
from wallace.weighted_selection import WeightedSelection
from wallace.parameters import ParameterSet

class DifferentialEvolution(OptimizationAlgorithm):
    def __init__(self, dataset, dependent_variable, settings, predictive_model_generator):
        OptimizationAlgorithm.__init__(self, dataset, dependent_variable, settings, predictive_model_generator)
        self.category_parameter_weights = {}

    def update_population(self):
        updated_population = []
        for target_model in self.model_population:
            parameter_selection = DEParameterSelection(self.settings, target_model, self.model_population, self.full_validity_check)
            parameter_set = parameter_selection.generate_parameter_set()

            independent_variable_selection = DEIndependentVariableSelection(self.settings, target_model, self.model_population, self.dataset)
            independent_variables = independent_variable_selection.generate_independent_variables()

            model_information = self.predictive_model_generator.choose_model_type()
            model_class = model_information["model_class"]

            updated_model = model_class(self.settings, parameter_set, self.dependent_variable, independent_variables)

            if self.evaluate_fitness(updated_model) <= self.evaluate_fitness(target_model):
                updated_population.append(updated_model)
            else:
                updated_population.append(target_model)

        self.model_population = updated_population

    def initialize_independent_variables(self):
        raise NotImplementedError()

class DESelection(object):
    def __init__(self, settings):
        self.settings = settings

    def generate_distinct(self, target, population, num_distinct=3):
        population = list(population)
        population.remove(target_model)
        return random.sample(population, num_models)

    def mutate(self, param1, param2, param3):
        rand = random.rand()
        if rand < self.crossover_probability():
            return param1 + self.differential_weight()*(param2 - param3)

    def crossover_probability(self):
        return self.settings.get("differential_evolution.crossover_probability")

    def differential_weight(self):
        return self.settings.get("differential_evolution.differential_weight")

class DEParameterSelection(object):
    def __init__(self, settings, target_model, model_population, validity_check):
        self.settings = settings
        self.target_model = target_model
        self.model_population = self.model_population
        self.validity_check = validity_check

    def generate_parameter_set(self):
        parameter_values = {}
        for parameter_name in self.validity_check.list_parameter_names():
            parameter_type = self.validity_check.get_parameter_type(parameter_name)
            if parameter_type == "CategoryParameter" or parameter_type == "IntegerRangeParameter":
                updated_value = self.validity_check.get_valid_value(parameter_name)
            else:
                de_selection = DESelection(self.settings)
                model1, model2, model3 = de_selection.generate_distinct(self.target_model, self.model_population, 3)
                param1 = model1.parameter_set.get(parameter_name)
                param2 = model2.parameter_set.get(parameter_name)
                param3 = model3.parameter_set.get(parameter_name)
                updated_value = de_selection.mutate(param1, param2, param3)

                if updated_value == None:
                    updated_value = self.target_model.parameter_set.get(parameter_name)
                elif not self.validity_check.check_validity(parameter_name, updated_value).is_valid:
                    updated_value = self.validity_check.get_valid_value(parameter_name)

            parameter_values[parameter_name] = updated_value
        return ParameterSet(parameter_values, validity_check=self.validity_check)

class DEIndependentVariableSelection(object):
    def __init__(self, target_model, model_population, dataset):
        self.target_model = target_model
        self.model_population = model_population
        self.dataset = dataset

    def generate_independent_variables(self):
        # TODO: implement this
        independent_variables = []
        for variable in self.dataset.
        pass
