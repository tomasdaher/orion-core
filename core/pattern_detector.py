from collections import Counter


class PatternDetector:

    def __init__(self, memory_service):
        self.memory_service = memory_service

    def detect_repeated_pipelines(self):

        executions = self.memory_service.get_recent_executions(20)

        pipelines = []

        for execution in executions:

            if "plan" in execution:
                pipelines.append(tuple(execution["plan"]))

        counts = Counter(pipelines)

        repeated = []

        for pipeline, count in counts.items():

            if count >= 3:
                repeated.append(list(pipeline))

        return repeated
