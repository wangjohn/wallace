from optimization_algorithm_stage import OptimizationAlgorithmStage

class InitializationStage(OptimizationAlgorithmStage):
    def __init__(self, settings):
        self.settings = settings

    def on_step(self, optimization_algorithm=None, payload=None):
        # Make sure the generator is only using OLS models.
        pass
