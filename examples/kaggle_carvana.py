import wallace
from wallace.initialization import WallaceInitialization

settings = {
    "fitness_evaluation.crossfold_partitions": 10,
    "model_tracking.models_to_track": 50,

    "differential_evolution.crossover_probability": 0.5,
    "differential_evolution.differential_weight": 0.8,

    "independent_variable_selection.initial_independent_variables_percentage": 0.25,

    "optimization_algorithm.population_size": 40,
    "optimization_algorithm.finishing_criteria.max_steps": 100
    }

dependent_variable = "IsBadBuy"
dataset_filename = "~/datasets/kaggle_carvana_training.csv"

WallaceInitialization.initialize(settings, dependent_variable, dataset_filename)
