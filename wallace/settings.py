class Settings(object):
    pass

class DifferentialEvolutionSettings(Settings):
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

