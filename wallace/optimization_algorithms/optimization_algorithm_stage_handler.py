from wallace.interval_storage import IntervalStorage

class OptimizationAlgorithmStageHandler(object):
    def __init__(self, settings, stages=None):
        self.settings = settings

        if stages == None:
            stages = self.settings.get("optimization_algoritm.default_stages")
        self.stage_storage = IntervalStorage(stages)

    def add_stage(self, stage, start_percentage, end_percentage):
        self.stage_storage.add_interval(stage, start_percentage, end_percentage)

    def has_stage(self, current_step, total_steps=None):
        step_percentage = self._get_step_percentage(current_step, total_steps)
        return self.stage_storage.has_entry(step_percentage)

    def get_stage(self, current_step, total_steps=None):
        step_percentage = self._get_step_percentage(current_step, total_steps)
        return self.stage_storage.get_entry(step_percentage)

    def _get_step_percentage(self, current_step, total_steps=None):
        if total_steps == None:
            total_steps = self.settings.get("optimization_algorithm.finishing_criteria.max_steps")
        return float(current_step) / total_steps
