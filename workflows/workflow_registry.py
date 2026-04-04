class WorkflowRegistry:

    def __init__(self):

        self.workflows = {}

    # ----------------------------
    # REGISTER WORKFLOW
    # ----------------------------

    def register(self, name, workflow):

        self.workflows[name] = workflow

    # ----------------------------
    # GET WORKFLOW
    # ----------------------------

    def get(self, name):

        return self.workflows.get(name)

    # ----------------------------
    # LIST WORKFLOWS
    # ----------------------------

    def list(self):

        return list(self.workflows.keys())