class InitializationStage(object):
    def __init__(self, settings):
        self.settings = settings

    def on_step(self, optimization_algorithm=None, payload=None):
        # Make sure the generator is only using OLS models.
        pass
