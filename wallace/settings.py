class AbstractSettings(object):
    DEFAULTS = {}

    def __init__(self, settings=None):
        self.settings = {}
        if settings != None:
            for attribute_name, value in settings.iteritems():
                self.set_attribute(attribute_name, value)

    def _resolve_options_attribute(self, attribute_name, *args):
        if attribute_name in self.settings:
            attribute = self.settings[attribute_name]

            if hasattr(attribute, "__call__"):
                return attribute(*args)
            else:
                return attribute
        elif attribute_name in self.DEFAULTS:
            return self.DEFAULTS[attribute_name]
        else:
            raise ValueError("Settings have no attribute '%s'" % attribute_name)

    def set_attribute(self, attribute_name, value):
        if attribute_name not in self.settings:
            getter_method = lambda self, *args : self._resolve_options_attribute(attribute_name, *args)
            setattr(self.__class__, attribute_name, getter_method)
        self.settings[attribute_name] = value

    @classmethod
    def set_default(cls, attribute_name, value):
        cls.DEFAULTS[attribute_name] = value
        getter_method = lambda self : self._resolve_options_attribute(attribute_name)
        setattr(cls, attribute_name, getter_method)

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

