class IntervalStorage(object):
    def __init__(self, interval_map=None):
        if interval_map == None:
            self.interval_map = {}
        else:
            if not isinstance(interval_map, dict):
                raise ValueError("Interval map must be a dictionary containing entries as keys and interval tuples as values.")

            self.interval_map = interval_map

    def add_interval(self, entry, start, end):
        self.validate_interval(start, end)
        self.interval_map[entry] = (start, end)

    def get_entry(self, point):
        for entry, interval in self.interval_map.iteritems():
            start, end = interval[0], interval[1]
            if start <= point and point < end:
                return entry
        raise ValueError("Point '%s' is not contained in any stored interval." % point)

    def validate_interval(self, start, end):
        if start > end:
            raise ValueError("Start must be lower than end in a valid interval.")

        if start > 1 or start < 0 or end > 1 or end < 0:
            raise ValueError("Intervals must be subsets of the interval [0,1].")

        if self.has_intersection(start, end):
            raise ValueError("Intervals cannot have an intersection with intervals that already exist in the storage object.")

    def has_intersection(self, start, end):
        for value in self.interval_map.itervalues():
            if (value[0] <= start and start <= value[1]) or \
                    (value[0] <= end and end <= value[1]) or \
                    (start <= value[0] and value[1] <= end):
                return True
        return False
