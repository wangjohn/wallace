import random

from wallace.optimization_algorithms.optimization_algorithm import OptimizationAlgorithm
from wallace.weighted_selection import WeightedSelection
from wallace.parameters import ParameterSet

class DifferentialEvolution(OptimizationAlgorithm):
    def __init__(self, dataset, dependent_variable, settings, predictive_model_generator):
        OptimizationAlgorithm.__init__(self, dataset, dependent_variable, settings, predictive_model_generator)
        self.category_parameter_weights = {}

    def update_population(self):
        parameter_selection = DEParameterSelection(self.model_population, self.full_validity_check)
        parameter_set = parameter_selection.generate_parameter_set()
        model_information = self.predictive_model_generator.choose_model_type()
        model_class = model_information["model_class"]
        model_class(self.settings, parameter_set, self.dependent_variable, independent_variables)
        pass

    def initialize_independent_variables(self):
        raise NotImplementedError()

    def evaluate_population_fitness(self):
        pass

class DEParameterSelection(object):
    def __init__(self, model_population, validity_check):
        self.model_population = self.model_population
        self.validity_check = validity_check

    def generate_parameter_set(self):
        # TODO: implement this
        return ParameterSet(parameter_values, validity_check=self.validity_check)

class DEIndependentVariableSelection(object):
    def __init__(self, model_population, dataset):
        self.model_population = model_population
        self.dataset = dataset

    def generate_independent_variables(self):
        # TODO: implement this
        pass


class DifferentialEvolutionCrossover(object):
    def __init__(self, settings):
        self.settings = settings

    def crossover(self, mutant, target):
        raise Exception("Unimplemented")

class DifferentialEvolutionSelection(object):
    def __init__(self, settings):
        self.settings = settings

    def select(self, target, trial):
        if self.settings.fitness(target) < self.settings.fitness(trial):
            return target
        else:
            return trial

class DifferentialEvolutionMutation(object):
    def __init__(self, settings, population):
        self.settings = settings
        self.population = population

    def mutate(self, target):
        raise Exception("Unimplemented")

class DifferentialEvolutionVector(object):
    def __init__(self, settings):
        self.settings = settings
