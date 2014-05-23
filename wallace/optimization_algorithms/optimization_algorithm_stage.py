class OptimizationAlgorithmStageStorage(object):
    def __init__(self, settings,
            independent_variable_probabilities=None):
        self.settings = settings
        self.independent_variable_probabilities = independent_variable_probabilities

class OptimizationAlgorithmStage(object):
    def __init__(self, settings):
        self.settings = settings

    def name(self):
        raise NotImplementedError()

    def before_stage(self):
        pass

    def after_stage(self):
        pass

    def step(self):
        pass
