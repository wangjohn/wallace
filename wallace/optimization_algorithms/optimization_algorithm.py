from wallace import fitness_evaluation
from wallace.independent_variables import IndependentVariableSelection

class OptimizationAlgorithm(object):
    def __init__(self, dataset, dependent_variable, settings, predictive_model_generator):
        self.dataset = dataset
        self.dependent_variable = dependent_variable
        self.settings = settings
        self.predictive_model_generator = predictive_model_generator
        self.full_validity_check = self.predictive_model_generator.get_full_validity_check()

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

            independent_variable_selection = IndependentVariableSelection(self.settings, self.dataset, self.dependent_variable)
            independent_variables = independent_variable_selection.initialize_independent_variables()
            new_model = model_class(self.settings, parameter_set, self.dependent_variable, independent_variables)
            model_wrapper = OptimizationAlgorithmModelWrapper(new_model, independent_variable_selection)
            model_population.append(model_wrapper)

        self.model_population = model_population

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

    def evaluate_fitness(self, model):
        evaluation = fitness_evaluation.CrossValidationFitnessEvaluation(self.settings, model, self.dataset)
        fitness = evaluation.evaluate()
        self.model_tracking.insert(fitness, model)
        return fitness

class OptimizationAlgorithmModelWrapper(object):
    def __init__(self, model, independent_variable_selection):
        self.model = model
        self.independent_variable_selection = independent_variable_selection

class ModelTracking(object):
    def __init__(self, settings):
        self.settings = settings
        self.models_to_track = self.settings.get("model_tracking.models_to_track")
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
