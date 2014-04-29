import random

class WeightedSelection(object):
    def __init__(self, weighted_selections=None):
        if weighted_selections == None:
            self.weighted_selections = {}
        else:
            self.weighted_selections = weighted_selections

    def add_selection(self, selection, weight=None):
        self.weighted_selections[selection] = weight

    def normalize_weights(self, weighted_selections):
        non_weighted = 0
        total_weight = 0
        for weight in weighted_selections.itervalues():
            if weight == None:
                non_weighted += 1
            else:
                total_weight += weight

        if non_weighted == len(weighted_selections):
            return self._uniformly_weighted_selections(weighted_selections)

        average_weight = float(total_weight) / (len(weighted_selections) - non_weighted)
        total_weight += average_weight * non_weighted

        normalized_weights = {}
        for selection, weight in weighted_selections.iteritems():
            if weight == None:
                normalized_weight = float(average_weight) / total_weight
            else:
                normalized_weight = float(weight) / total_weight
            normalized_weights[selection] = normalized_weight

        return normalized_weights

    def _uniformly_weighted_selections(self, selections):
        normalized_weights = {}
        total_selections = len(selections)
        for selection in selections.iterkeys():
            normalized_weights[selection] = float(1) / total_selections
        return normalized_weights

    def choose(self, rand_generator=None, rand_number=None):
        normalized_weights = self.normalize_weights(self.weighted_selections)
        if rand_generator != None:
            rand = rand_generator()
        elif rand_number != None:
            rand = rand_number
        else:
            rand = random.random()

        current_sum = 0
        for selection, weight in normalized_weights.iteritems():
            if rand <= weight + current_sum:
                return selection
            current_sum += weight
