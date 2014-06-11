class OptimizationAlgorithmStageStorage(object):
    def __init__(self, settings,
            independent_variable_probabilities=None):
        self.settings = settings
        self.independent_variable_probabilities = independent_variable_probabilities

class OptimizationAlgorithmStage(object):
    def __init__(self, settings):
        self.settings = settings

    def before_stage(self, payload=None):
        pass

    def after_stage(self, payload=None):
        pass

    def on_step(self, payload=None):
        if "optimization_algorithm" in payload:
            optimization_algorithm = payload["optimization_algorithm"]

            if optimization_algorithm.initialized_population:
                optimization_algorithm.update_population()
            else:
                optimization_algorithm.initialize_population()

    def _get_optimization_algorithm(self, payload):
        if "optimization_algorithm" in payload:
            return payload["optimization_algorithm"]
        else:
            raise ValueError("You must specify `optimization_algorithm` in the payload for InitializationStage methods.")

