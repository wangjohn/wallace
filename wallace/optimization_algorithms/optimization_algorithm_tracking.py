import json

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
        self.flush_data(step_number)

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

    def flush_data(self, step_number=None, filename=None):
        step_number = self._get_step_number(step_number)
        if filename == None:
            filename = self.settings.get("optimization_algorithm_tracking.tracking_log_filename")

        step_population = self.population_history[step_number]
        data = {
                "step": step_number,
                "model_population": step_population
                }

        with open(filename, 'a+') as f:
            f.write(json.dumps(data) + "\n")

    def read_logging_file(self, filename=None):
        if filename == None:
            filename = self.settings.get("optimization_algorithm_tracking.tracking_log_filename")

        logging_file_results = []
        with open(filename, 'r') as f:
            for line in f:
                logging_file_results.append(json.loads(line))
        return logging_file_results


