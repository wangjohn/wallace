class OptimizationAlgorithm(object):
    def __init__(self, dataset, settings):
        self.dataset = dataset
        self.settings = settings

        self.model_population = []
        self.current_step = 0
        self.model_tracking = ModelTracking(self.settings)

    def initialize_population(self):
        raise NotImplementedError()

    def update_population(self):
        raise NotImplementedError()

    def has_finished(self):
        raise NotImplementedError()

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
            fitness = model.evaluate_fitness(self.dataset)
            self.model_tracking.insert(fitness, model)

class ModelTracking(object):
    def __init__(self, settings):
        self.models_to_track = self.settings.models_to_track()
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
