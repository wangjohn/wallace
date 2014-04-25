class DifferentialEvolution(object):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

    def step(self):
        pass

class Dataset(object):
    def __init__(self, data_matrix, headers=None):
        self.headers = headers
        self.data_matrix = data_matrix
        self.rows = len(self.data_matrix)

    def get(self, row, col):
        return self.data_matrix[row][col]

    def get_with_header(self, row, header):
        col = self.column_from_header(header)
        return self.get(row, col)

    def column_index(self, header):
        for i in xrange(len(self.headers)):
            if self.headers[i] == header:
                return i

    def get_column(self, col):
        for row in xrange(self.rows):
            yield self.data_matrix[row][col]

    def get_column_with_header(self, header):
        col = self.column_index(header)
        return self.get_column(col)

    def get_row(self, row):
        return self.data_matrix[row]

class DifferentialEvolutionSettings(object):
    DEFAULT_CROSSOVER_PROBABILITY = 0.5
    DEFAULT_DIFFERENTIAL_WEIGHT = 0.8
    DEFAULT_POPULATION_SIZE = 10

    def __init__(self, options):
        self.options = options

    def crossover_probability(self, extra_data=None):
        default = self.DEFAULT_CROSSOVER_PROBABILITY
        return self._resolve_options_attribute("crossover_probability", default, extra_data)

    def differential_weight(self, extra_data=None):
        default = self.DEFAULT_DIFFERENTIAL_WEIGHT
        return self._resolve_options_attribute("differential_weight", default, extra_data)

    def population_size(self, extra_data=None):
        default = self.DEFAULT_POPULATION_SIZE
        return self._resolve_options_attribute("population_size", default, extra_data)

    def _resolve_options_attribute(self, attribute_name, default):
        if attribute_name in self.options:
            attribute = self.options[attribute_name]

            if hasattr(attribute, "__call__"):
                return attribute(extra_data)
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
