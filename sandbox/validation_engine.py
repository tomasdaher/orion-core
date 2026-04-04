import logging


class ValidationEngine:

    def __init__(self):

        self.logger = logging.getLogger("Orion")

    def validate(self, execution_result):

        if not execution_result["success"]:

            return {
                "approved": False,
                "reason": "execution_failed"
            }

        execution_time = execution_result.get("execution_time", 999)

        if execution_time > 5:

            return {
                "approved": False,
                "reason": "too_slow"
            }

        return {
            "approved": True,
            "reason": "valid_capability"
        }