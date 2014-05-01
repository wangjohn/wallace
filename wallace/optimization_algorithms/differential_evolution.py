import random

from wallace.optimization_algorithms.optimization_algorithm import OptimizationAlgorithm
from wallace.weighted_selection import WeightedSelection

class DifferentialEvolution(OptimizationAlgorithm):
    def __init__(self, dataset, dependent_variable, settings, predictive_model_generator):
        OptimizationAlgorithm.__init__(self, dataset, dependent_variable, settings, predictive_model_generator)
        self.category_parameter_weights = {}

    def update_population(self):
        parameter_weights = {}
        chosen_models = random.sample(self.model_population, 3)
        pass

    def initialize_independent_variables(self):
        raise NotImplementedError()

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
