import logging


class LeadSource:

    name = "acquire_lead"

    def execute(self, state):

        logging.info("🔎 Acquiring lead from environment")

        # simulación de obtención desde environment
        environment = state.get("environment")

        if environment:

            lead = environment.get_new_lead()

        else:

            lead = {
                "name": "unknown",
                "email": "unknown@unknown.com",
                "company": None,
                "source": "simulation"
            }

        state["data"] = lead

        return state


def acquire_lead(state):

    handler = LeadSource()

    return handler.execute(state)