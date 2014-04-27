class AbstractSettings(object):
    def __init__(self, options):
        self.options = options

    def _resolve_options_attribute(self, attribute_name, default):
        if attribute_name in self.options:
            attribute = self.options[attribute_name]

            if hasattr(attribute, "__call__"):
                return attribute(extra_data)
            else:
                return attribute

        return default

class FitnessEvaluationSettings(AbstractSettings):
    DEFAULT_CROSS_FOLD_PARTITIONS = 10

    def cross_fold_partitions(self, extra_data=None):
        default = self.DEFAULT_CROSS_FOLD_PARTITIONS
        return self._resolve_options_attribute("cross_fold_partitions", default, extra_data)

class ModelTrackingSettings(AbstractSettings):
    DEFAULT_MODELS_TO_TRACK = 50

    def models_to_track(self, extra_data=None):
        default = self.DEFAULT_MODELS_TO_TRACK
        return self._resolve_options_attribute("models_to_track", default, extra_data)

class DifferentialEvolutionSettings(AbstractSettings):
    DEFAULT_CROSSOVER_PROBABILITY = 0.5
    DEFAULT_DIFFERENTIAL_WEIGHT = 0.8
    DEFAULT_POPULATION_SIZE = 10

    def crossover_probability(self, extra_data=None):
        default = self.DEFAULT_CROSSOVER_PROBABILITY
        return self._resolve_options_attribute("crossover_probability", default, extra_data)

    def differential_weight(self, extra_data=None):
        default = self.DEFAULT_DIFFERENTIAL_WEIGHT
        return self._resolve_options_attribute("differential_weight", default, extra_data)

    def population_size(self, extra_data=None):
        default = self.DEFAULT_POPULATION_SIZE
        return self._resolve_options_attribute("population_size", default, extra_data)

