class OptimizationAlgorithmTracking(object):
    def __init__(self, settings):
        self.settings = settings
        self.population_history = {}
        self.best_fitness_history = {}
        self.current_step = None

    def track_step(self, step_number, model_population):
        self.current_step = step_number
        self.population_history[step_number] = [wrapper.json() for wrapper in model_population]
        self.best_fitness_history[step_number] = max([wrapper.fitness for wrapper in model_population])

    def step_population_history(self, step_number=None):
        step_number = self._get_step_number(step_number)
        return self.population_history[step_number]

    def step_fitness_history(self, step_number=None):
        step_number = self._get_step_number(step_number)
        return self.best_fitness_history[step_number]

    def _get_step_number(self, step_number):
        if step_number == None:
            step_number = self.current_step
        if step_number not in self.population_history:
            raise ValueError("Step '%s' is not in the tracking history." % step_number)

        return step_number
