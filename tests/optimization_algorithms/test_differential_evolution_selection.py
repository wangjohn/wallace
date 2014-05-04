from unittest import TestCase

from wallace.optimization_algorithms.differential_evolution import DESelection
from wallace.settings import AbstractSettings

class DESelectionTest(TestCase):
    def setUp(self):
        settings = AbstractSettings({
            "differential_evolution.crossover_probability": 1.0,
            "differential_evolution.differential_weight": 1.0
            })
        self.de_selection = DESelection(settings)

    def test_generate_distinct_instances_from_population(self):
        population = ["0","1","2","3"]
        target = population[0]
        generated = self.de_selection.generate_distinct(target, population, 3)

        self.assertEqual(3, len(generated))
        self.assertIn("1", generated)
        self.assertIn("2", generated)
        self.assertIn("3", generated)

    def test_generate_distinct_instances_from_undersized_population(self):
        population = ["0", "1"]
        target = population[0]
        with self.assertRaises(ValueError):
            generated = self.de_selection.generate_distinct(target, population, 3)

    def test_mutate_parameters(self):
        params = [1.0, 1.5, 2.0]
        result = self.de_selection.mutate(*params)

        self.assertEqual(0.5, result)

    def test_mutate_parameters_without_crossover_probability(self):
        settings = AbstractSettings({
            "differential_evolution.crossover_probability": 0.0,
            "differential_evolution.differential_weight": 1.0
            })
        de_selection = DESelection(settings)
        params = [1.0, 1.5, 2.0]
        result = de_selection.mutate(*params)

        self.assertEqual(None, result)
