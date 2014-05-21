import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
        sys.path.insert(1, path)

from wallace.initialization import WallaceInitialization

settings = {
    "independent_variable_selection.initial_independent_variables_percentage": 0.25,
    "optimization_algorithm.population_size": 40,
    "optimization_algorithm.finishing_criteria.max_steps": 200,
    "optimization_algorithm_tracking.final_results_filename": "final_results.log"
    }

dependent_variable = "IsBadBuy"
dataset_filename = os.path.join(os.path.dirname(__file__), "../example_datasets/carvana_example.csv")

WallaceInitialization.initialize(settings, dependent_variable, dataset_filename)
