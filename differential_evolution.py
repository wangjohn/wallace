class DifferentialEvolution(object):
    def __init__(self, dataset, settings):
        self.dataset = dataset
        self.settings = settings
        self.population = None

    def initialize(self):
        self.population = []


    def step(self):

        pass

class DifferentialEvolutionPopulation(object):
    def __init__(self, settings):
        self.settings = settings

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
