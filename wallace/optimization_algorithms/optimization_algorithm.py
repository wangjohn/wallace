from wallace.fitness_evaluation import CrossValidationFitnessEvaluation
from wallace.independent_variables import IndependentVariableSelection
from wallace.optimization_algorithms.optimization_algorithm_model_wrapper import OptimizationAlgorithmModelWrapper
from wallace.optimization_algorithms.optimization_algorithm_tracking import OptimizationAlgorithmTracking
from wallace.results_logger import ResultsLogger
import logging
import heapq

class OptimizationAlgorithm(object):
    def __init__(self, dataset, dependent_variable, settings, predictive_model_generator):
        self.dataset = dataset
        self.dependent_variable = dependent_variable
        self.settings = settings
        self.predictive_model_generator = predictive_model_generator
        self.full_validity_check = self.predictive_model_generator.get_full_validity_check()
        self.logger = logging.getLogger(__name__)

        self.model_population = []
        self.current_step = 0
        self.model_tracking = ModelTracking(self.settings)
        self.optimization_algorithm_tracking = OptimizationAlgorithmTracking(self.settings)
        self.results_logger = ResultsLogger(self.settings, self.model_tracking)

    def initialize_population(self):
        model_population = []
        population_size = self.settings.get("optimization_algorithm.population_size")
        for i in xrange(population_size):
            model_information = self.predictive_model_generator.choose_model_type()
            model_class = model_information["model_class"]
            parameter_set = self.predictive_model_generator.get_full_parameter_set()

            independent_variable_selection = IndependentVariableSelection(
                    self.settings,
                    self.dependent_variable,
                    self.dataset.get_independent_variables(self.dependent_variable))
            independent_variables = independent_variable_selection.initialize_independent_variables()

            new_model = model_class(
                    self.settings,
                    parameter_set,
                    self.dependent_variable,
                    independent_variables)
            model_wrapper = OptimizationAlgorithmModelWrapper(new_model, independent_variable_selection)
            model_population.append(model_wrapper)

        self.model_population = model_population
        self.logger.info("Initialized optimization algorithm with population size %s", population_size)

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

        self.results_logger.write_results()
        self.logger.info("Finished running optimization algorithm.")

    def step(self):
        self.current_step += 1
        self.update_population()
        self.optimization_algorithm_tracking.track_step(self.current_step, self.model_population)
        self.results_logger.write_results()
        self.logger.info("Optimization algorithm step: %s", self.current_step)

    def evaluate_fitness(self, model, evaluation_method=None):
        if evaluation_method == None:
            evaluation_method = self.settings.get("fitness_evaluation.evaluation_method")

        evaluation = CrossValidationFitnessEvaluation(self.settings, model, self.dataset)

        if evaluation_method.evaluation_type() == "maximizer":
            fitness = -evaluation.evaluate(evaluation_method)
        elif evaluation_method.evaluation_type() == "minimizer":
            fitness = evaluation.evaluate(evaluation_method)
        else:
            raise ValueError("Invalid evaluation type '%s'" % evaluation_method.evaluation_type)

        self.model_tracking.insert(fitness, model)
        return fitness

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
        return [(model, -negative_fitness) for negative_fitness, model in best_models]

    def best_fitness(self):
        best_models = sorted(self.best_models, reverse=True)
        return -best_models[0][0]
