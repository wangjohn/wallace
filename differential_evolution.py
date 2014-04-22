class DifferentialEvolution(object):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

    def step(self):
        pass

class DifferentialEvolutionSettings(object):
    DEFAULT_CROSSOVER_PROBABILITY = 0.5
    DEFAULT_DIFFERENTIAL_WEIGHT = 0.8
    DEFAULT_POPULATION_SIZE = 10

    def __init__(self, options):
        self.options = options

    def crossover_probability(self, step=None):
        default = self.DEFAULT_CROSSOVER_PROBABILITY
        return self._resolve_options_attribute("crossover_probability", default)

    def differential_weight(self, step=None):
        default = self.DEFAULT_DIFFERENTIAL_WEIGHT
        return self._resolve_options_attribute("differential_weight", default)

    def population_size(self, step=None):
        default = self.DEFAULT_POPULATION_SIZE
        return self._resolve_options_attribute("population_size", default)

    def _resolve_options_attribute(self, attribute_name, default):
        if attribute_name in self.options:
            attribute = self.options[attribute_name]

            if hasattr(attribute, "__call__"):
                return attribute()
            else:
                return attribute

        return default


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

class DifferentialEvolutionPopulation(object):
    def __init__(self, settings):
        self.settings = settings

class DifferentialEvolutionVector(object):
    def __init__(self, settings):
        self.settings = settings
