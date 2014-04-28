class AbstractSettings(object):
    DEFAULTS = {
            "fitness_evaluation_crossfold_partitions": 10,
            "model_tracking_models_to_track": 50,
            "differential_evolution_crossover_probability": 0.5,
            "differential_evolution_differential_weight": 0.8,
            "differential_evolution_population_size": 20
        }

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
    def set_default(klass, attribute_name, value):
        klass.DEFAULTS[attribute_name] = value
        getter_method = lambda self : self._resolve_options_attribute(attribute_name)
        setattr(klass, attribute_name, getter_method)
