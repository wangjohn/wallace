import random
from wallace.optimization_algorithms.optimization_algorithm import OptimizationAlgorithm

class DifferentialEvolution(OptimizationAlgorithm):
    def __init__(self, dataset, settings):
        OptimizationAlgorithm.__init__(self, dataset, settings)

    def update_population(self):
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
