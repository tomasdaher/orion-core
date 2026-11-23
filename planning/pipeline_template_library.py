class PipelineTemplateLibrary:

    def __init__(self):

        self.templates = {

            "increase_lead_conversion": [
                "acquire_lead",
                "capture_lead",
                "clean_data",
                "classify_lead",
                "score_lead",
                "store_lead",
                "notify_sales"
            ],

            "lead_automation": [
                "capture_lead",
                "clean_data",
                "classify_lead",
                "store_lead"
            ],

            "optimize_pipeline": [
                "analyze_input",
                "validate_data",
                "execute_task",
                "explore_optimization"
            ]

        }

    def get_template(self, goal_name):

        return self.templates.get(goal_name)