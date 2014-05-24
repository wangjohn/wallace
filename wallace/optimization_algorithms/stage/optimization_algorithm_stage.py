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
        pass
