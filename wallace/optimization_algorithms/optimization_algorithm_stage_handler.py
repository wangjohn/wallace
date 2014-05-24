from wallace.interval_storage import IntervalStorage

class OptimizationAlgorithmStageHandler(object):
    def __init__(self, settings, stages=None):
        self.settings = settings

        if stages == None:
            stages = self.settings.get("optimization_algoritm.default_stages")
        self.stage_storage = IntervalStorage(stages)
        self.stages_used = []

    def add_stage(self, stage, start_percentage, end_percentage):
        self.stage_storage.add_interval(stage, start_percentage, end_percentage)

    def has_stage(self, current_step, total_steps=None):
        step_percentage = self._get_step_percentage(current_step, total_steps)
        return self.stage_storage.has_entry(step_percentage)

    def get_stage(self, current_step, total_steps=None):
        step_percentage = self._get_step_percentage(current_step, total_steps)
        return self.stage_storage.get_entry(step_percentage)

    def run_stage(self, current_step, total_steps=None):
        stage = None
        if self.has_stage(curent_step, total_steps):
            stage = self.get_stage(current_step, total_steps)

        # If we've started using a new stage, check to see if we have to run the
        # `after_stage` method.
        if stage == None or stage not in self.stages_used:
            last_stage, has_run_after_stage = self.stages_used[-1]
            if not has_run_after_stage:
                last_stage.after_stage()
                self.stages_used[-1] = (last_stage, True)

        # If this is the first time we've seen the stage, then run the `before_stage`
        # method
        if stage not in self.stages_used:
            stage.before_stage()
            self.stages_used.append((stage, False))

        # Run the stage if it exists
        if stage != None:
            stage.on_step()

    def _get_step_percentage(self, current_step, total_steps=None):
        if total_steps == None:
            total_steps = self.settings.get("optimization_algorithm.finishing_criteria.max_steps")
        return float(current_step) / total_steps
