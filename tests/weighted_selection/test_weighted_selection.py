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

    def test_weight_increase_without_tapering(self):
        selections = {"1": None, "2": None, "3": None, "4": None, "5": None}

        weighted_selection = WeightedSelection(selections)
        weighted_selection.increase_weight("1", learning_parameter=0.5, taper=False)
        selections = weighted_selection.weighted_selections

        self.assertAlmostEqual(0.272727272727, selections["1"])
        self.assertAlmostEqual(0.181818181818, selections["2"])
        self.assertAlmostEqual(0.181818181818, selections["3"])
        self.assertAlmostEqual(0.181818181818, selections["4"])
        self.assertAlmostEqual(0.181818181818, selections["5"])

    def test_weight_increase_with_tapering(self):
        selections = {"1": None, "2": None, "3": None, "4": None, "5": None}

        weighted_selection = WeightedSelection(selections)
        weighted_selection.increase_weight("1", learning_parameter=0.5, taper=True)
        selections = weighted_selection.weighted_selections

        self.assertAlmostEqual(0.259259259259, selections["1"])
        self.assertAlmostEqual(0.185185185185, selections["2"])
        self.assertAlmostEqual(0.185185185185, selections["3"])
        self.assertAlmostEqual(0.185185185185, selections["4"])
        self.assertAlmostEqual(0.185185185185, selections["5"])

    def test_sample_from_simple_weighted_selection(self):
        selections = {"1": None, "2": None}
        weighted_selection = WeightedSelection(selections)

        sampled_results = WeightedSelection.sample(weighted_selection, 2)
        self.assertEqual(2, len(sampled_results))
        self.assertIn("1", sampled_results)
        self.assertIn("2", sampled_results)

    def test_sample_raises_error_when_sample_is_larger_than_population(self):
        selections = {"1": None, "2": None}
        weighted_selection = WeightedSelection(selections)

        with self.assertRaises(ValueError):
            sampled_results = WeightedSelection.sample(weighted_selection, 3)

    def test_sample_from_large_population_with_zero_probabilities(self):
        selections = {}
        for i in xrange(1000):
            selections[i] = 0
        selections[0] = 0.5
        selections[1] = 0.5

        weighted_selection = WeightedSelection(selections)
        sampled_results = WeightedSelection.sample(weighted_selection, 2)

        self.assertEqual(2, len(sampled_results))
        self.assertIn(0, sampled_results)
        self.assertIn(1, sampled_results)
