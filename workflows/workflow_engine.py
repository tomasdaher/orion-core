class WorkflowEngine:

    def __init__(self, workflow_registry):

        self.registry = workflow_registry

    # --------------------------------
    # MATCH WORKFLOW
    # --------------------------------

    def match_workflow(self, input_data):

        trigger = input_data.get("trigger")

        for name in self.registry.list():

            workflow = self.registry.get(name)

            if workflow.get("trigger") == trigger:

                return workflow

        return None

    # --------------------------------
    # BUILD EXECUTION PLAN
    # --------------------------------

    def build_plan(self, workflow):

        steps = []

        for action in workflow.get("actions", []):

            steps.append(action)

        return steps