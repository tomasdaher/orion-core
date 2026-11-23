import logging


def score_lead(state):

    lead = state.get("lead")

    if not lead:
        logging.warning("⚠️ No lead found for scoring")
        return state

    score = 0

    # ------------------------------------------------
    # EMAIL VALIDATION
    # ------------------------------------------------

    email = getattr(lead, "email", "")

    if "@" in email:
        score += 30

    if email.endswith(".com"):
        score += 20

    # ------------------------------------------------
    # LEAD TYPE
    # ------------------------------------------------

    lead_type = getattr(lead, "type", "")

    if lead_type == "business":
        score += 30

    # ------------------------------------------------
    # SOURCE
    # ------------------------------------------------

    source = getattr(lead, "source", "")

    if source == "web":
        score += 20

    # ------------------------------------------------
    # SAVE SCORE
    # ------------------------------------------------

    setattr(lead, "score", score)

    logging.info(f"⭐ Lead scored: {score}")

    return state