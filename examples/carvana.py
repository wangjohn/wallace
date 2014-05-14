import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
        sys.path.insert(1, path)

from wallace.initialization import WallaceInitialization

settings = {
    "fitness_evaluation.crossfold_partitions": 10,
    "model_tracking.models_to_track": 50,

    "differential_evolution.crossover_probability": 0.5,
    "differential_evolution.differential_weight": 0.8,

    "independent_variable_selection.initial_independent_variables_percentage": 0.25,

    "optimization_algorithm.population_size": 40,
    "optimization_algorithm.finishing_criteria.max_steps": 2
    }

dependent_variable = "IsBadBuy"
dataset_filename = os.path.join(os.path.dirname(__file__), "../example_datasets/carvana_example.csv")

WallaceInitialization.initialize(settings, dependent_variable, dataset_filename)
