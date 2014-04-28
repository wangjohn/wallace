from wallace.optimization_algorithms import OptimizationAlgorithm

class DifferentialEvolution(OptimizationAlgorithm):
    def __init__(self, dataset, settings):
        OptimizationAlgorithm.__init__(self, dataset, settings)

    def initialize_population(self):
        self.population = []

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
