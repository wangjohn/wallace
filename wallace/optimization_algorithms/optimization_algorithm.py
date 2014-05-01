from wallace import fitness_evaluation

class OptimizationAlgorithm(object):
    def __init__(self, dataset, dependent_variable, settings, predictive_model_generator):
        self.dataset = dataset
        self.dependent_variable = dependent_variable
        self.settings = settings
        self.predictive_model_generator = predictive_model_generator

        self.model_population = []
        self.current_step = 0
        self.model_tracking = ModelTracking(self.settings)

    def initialize_population(self):
        model_population = []
        population_size = self.settings.get("optimization_algorithm.population_size")
        for i in xrange(population_size):
            model_information = self.predictive_model_generator.choose_model_type()
            model_class = model_information["model_class"]
            parameter_set = self.predictive_model_generator.get_full_parameter_set()

            independent_variables = self.initialize_independent_variables()
            new_model = model_class(self.settings, parameter_set, self.dependent_variable, independent_variables)
            model_population.append(new_model)

        self.model_population = model_population

    def initialize_independent_variables(self):
        raise NotImplementedError()

    def update_population(self):
        raise NotImplementedError()

    def has_finished(self):
        max_steps = "optimization_algorithm.finishing_criteria.max_steps"
        if self.settings.has(max_steps) and \
                self.current_step >= self.settings.get(max_steps):
            return True

        fitness_threshold = "optimization_algorithm.finishing_criteria.fitness_threshold"
        if self.settings.has(fitness_threshold) and \
                self.model_tracking.best_fitness_level() < self.settings.get(fitness_threshold):
            return True

        return False

    def run(self):
        self.initialize_population()

        while not self.has_finished():
            self.step()

    def step(self):
        self.current_step += 1
        self.update_population()
        self.evaluate_population_fitness()

    def evaluate_population_fitness(self):
        for model in self.model_population:
            evaluation = fitness_evaluation.CrossValidationFitnessEvaluation(self.settings, model, self.dataset)
            fitness = evaluation.evaluate()
            self.model_tracking.insert(fitness, model)

class ModelTracking(object):
    def __init__(self, settings):
        self.models_to_track = self.settings.model_tracking_models_to_track()
        self.best_models = []

    def insert(self, fitness, model):
        if model not in self.best_models:
            if len(self.best_models) > self.models_to_track:
                heapq.heappushpop(self.best_models, (-fitness, model))
            else:
                heapq.heappush(self.best_models, (-fitness, model))

    def best_models(self):
        best_models = sorted(self.best_models, reverse=True)
        for negative_fitness, model in best_models:
            yield (-negative_fitness, model)

    def best_fitness(self):
        best_models = sorted(self.best_models, reverse=True)
        return -best_models[0][0]
