class OptimizationAlgorithmTracking(object):
    def __init__(self, settings):
        self.settings = settings
        self.history = {}
        self.current_step = None

    def track_step(self, step_number, model_population):
        self.current_step = step_number
        self.history[step_number] = [wrapper.json() for model in model_population]

    def step_results(self, step_number=None):
        if step_number == None:
            step_number = self.current_step
        if step_number not in self.history:
            raise ValueError("Step '%s' is not in the tracking history." % step_number)

        return self.history[step_number]

