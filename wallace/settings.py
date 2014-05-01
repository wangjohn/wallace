class AbstractSettings(object):
    DEFAULTS = {
            "fitness_evaluation.crossfold_partitions": 10,
            "model_tracking.models_to_track": 50,
            "differential_evolution.crossover_probability": 0.5,
            "differential_evolution.differential_weight": 0.8,
            "optimization_algorithm.population_size": 40
        }

    def __init__(self, settings=None):
        self.settings = {}
        if settings != None:
            for attribute_name, value in settings.iteritems():
                self.set(attribute_name, value)

    def _resolve_attribute(self, attribute, *args):
        if hasattr(attribute, "__call__"):
            return attribute(*args)
        else:
            return attribute

    def set(self, attribute_name, value):
        self.settings[attribute_name] = value

    def get(self, attribute_name, *args):
        if attribute_name in self.settings:
            return self._resolve_attribute(self.settings[attribute_name], *args)
        elif attribute_name in self.DEFAULTS:
            return self._resolve_attribute(self.DEFAULTS[attribute_name], *args)
        else:
            raise ValueError("Settings have no attribute '%s'" % attribute_name)

    def has(self, attribute_name):
        return (attribute_name in self.settings) or (attribute_name in self.DEFAULTS)

    @classmethod
    def set_default(klass, attribute_name, value):
        klass.DEFAULTS[attribute_name] = value
