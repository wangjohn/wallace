from wallace.fitness_evaluation_methods.fitness_evaluation_method import MeanSquaredError

class AbstractSettings(object):
    DEFAULTS = {
            "fitness_evaluation.crossfold_partitions": 10,
            "fitness_evaluation.evaluation_method": MeanSquaredError,
            "model_tracking.models_to_track": 50,
            "optimization_algorithm_tracking.tracking_log_filename": "logs/optimization_algorithm_logs.log"
            "dataset.maximum_dataset_size": 50000,
            "dataset.randomize_file_reader": False,
            "dataset.remove_rows_with_missing_data": True,
            "differential_evolution.crossover_probability": 0.5,
            "differential_evolution.differential_weight": 0.8,
            "optimization_algorithm.population_size": 40,
            "independent_variable_selection.initial_independent_variables_percentage": 0.25
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
