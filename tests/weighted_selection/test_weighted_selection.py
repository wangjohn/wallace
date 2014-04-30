from unittest import TestCase

from wallace.weighted_selection import WeightedSelection

class WeightedSelectionTest(TestCase):
    def test_single_weight_normalization(self):
        selections = {"1": 0.5}

        weighted_selection = WeightedSelection(selections)
        normalized = weighted_selection.normalize_weights(selections)

        self.assertAlmostEqual(1.0, normalized["1"])

    def test_multiple_weight_normalization(self):
        selections = {"1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5}

        weighted_selection = WeightedSelection(selections)
        normalized = weighted_selection.normalize_weights(selections)

        self.assertAlmostEqual(0.25, normalized["1"])
        self.assertAlmostEqual(0.25, normalized["2"])
        self.assertAlmostEqual(0.25, normalized["3"])
        self.assertAlmostEqual(0.25, normalized["4"])

    def test_weight_normalization_with_none_weights(self):
        selections = {"1": 0.5, "2": 0.5, "3": None, "4": None}

        weighted_selection = WeightedSelection(selections)
        normalized = weighted_selection.normalize_weights(selections)

        self.assertAlmostEqual(0.25, normalized["1"])
        self.assertAlmostEqual(0.25, normalized["2"])
        self.assertAlmostEqual(0.25, normalized["3"])
        self.assertAlmostEqual(0.25, normalized["4"])

    def test_weight_normalization_without_any_weights(self):
        selections = {"1": None, "2": None, "3": None, "4": None, "5": None}

        weighted_selection = WeightedSelection(selections)
        normalized = weighted_selection.normalize_weights(selections)

        self.assertAlmostEqual(0.2, normalized["1"])
        self.assertAlmostEqual(0.2, normalized["2"])
        self.assertAlmostEqual(0.2, normalized["3"])
        self.assertAlmostEqual(0.2, normalized["4"])
