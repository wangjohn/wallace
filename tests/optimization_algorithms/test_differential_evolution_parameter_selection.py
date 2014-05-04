from unittest import TestCase

from wallace.optimization_algorithms.differential_evolution import DEParameterSelection
from wallace.settings import AbstractSettings

class DEParameterSelectionTest(TestCase):
    def setUp(self):
        settings_hash = {
            "differential_evolution.crossover_probability": 1.0,
            "differential_evolution.differential_weight": 1.0
            }
        settings = AbstractSettings(settings_hash)
        model_population = []

