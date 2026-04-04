class LeadScorer:

    name = "score_lead"

    def execute(self, state):

        lead = state.get("lead")

        if not lead:
            return state

        score = 0

        if lead.company:
            score += 40

        if lead.email:
            score += 30

        if lead.source == "web":
            score += 20

        lead.score = score

        print(f"📊 Lead scored: {score}")

        return state