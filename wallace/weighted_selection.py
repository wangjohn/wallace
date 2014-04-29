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
                total_weight += weight
            else:
                non_weighted += 1

        if non_weighted == len(weighted_selections):
            return None

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

    def choose(self):
        normalized_weights = self.normalize_weights(self.weighted_selections)
        if normalized_weights == None:
            return random.choice(self.weighted_selections.keys())
        else:
            rand = random.random()
            current_sum = 0
            for selection, weight in normalized_weights.iteritems():
                if rand <= weight + current_sum:
                    return selection
                current_sum += weight
