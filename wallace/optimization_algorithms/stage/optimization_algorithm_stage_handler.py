class OptimizationAlgorithmStageHandler(object):
    def __init__(self, settings, stages=None):
        self.settings = settings

        if stages == None:
            self.stages = self.settings.get("optimization_algoritm.default_stages")
        else:
            self.stages = stages

    def get_stage(self, current_step):
        total_steps = self.settings.get("optimization_algorithm.finishing_criteria.max_steps")
        step_percentage = float(current_step) / total_steps
