import re


class IntentInterpreter:

    def __init__(self):

        # ------------------------------------------------
        # GOAL DETECTION
        # ------------------------------------------------
        self.goal_patterns = {

            "lead_generation": [
                "lead",
                "leads",
                "prospects"
            ]

        }

        # ------------------------------------------------
        # SOURCE DETECTION
        # ------------------------------------------------
        self.source_patterns = {

            "instagram": [
                "instagram",
                "ig"
            ],

            "linkedin": [
                "linkedin"
            ],

            "web": [
                "website",
                "web"
            ]

        }

        # ------------------------------------------------
        # ACTION DETECTION
        # ------------------------------------------------
        self.action_patterns = {

            "capture": [
                "capture",
                "collect",
                "get"
            ],

            "clean": [
                "clean",
                "sanitize"
            ],

            "classify": [
                "classify",
                "score",
                "segment"
            ],

            "store": [
                "store",
                "save",
                "persist"
            ],

            "notify": [
                "notify",
                "alert",
                "inform"
            ]

        }

    # ============================================================
    # MAIN INTERPRET
    # ============================================================
    def interpret(self, text):

        text = text.lower()

        intent = {
            "goal": None,
            "source": None,
            "actions": [],
            "conditions": []
        }

        # ------------------------------------------------
        # GOAL
        # ------------------------------------------------
        intent["goal"] = self._detect_goal(text)

        # ------------------------------------------------
        # SOURCE
        # ------------------------------------------------
        intent["source"] = self._detect_source(text)

        # ------------------------------------------------
        # ACTIONS
        # ------------------------------------------------
        intent["actions"] = self._detect_actions(text)

        # ------------------------------------------------
        # CONDITIONS
        # ------------------------------------------------
        intent["conditions"] = self._detect_conditions(text)

        return intent

    # ============================================================
    # GOAL DETECTION
    # ============================================================
    def _detect_goal(self, text):

        for goal, patterns in self.goal_patterns.items():

            for pattern in patterns:

                if pattern in text:
                    return goal

        return "generic"

    # ============================================================
    # SOURCE DETECTION
    # ============================================================
    def _detect_source(self, text):

        for source, patterns in self.source_patterns.items():

            for pattern in patterns:

                if pattern in text:
                    return source

        return "generic"

    # ============================================================
    # ACTION DETECTION
    # ============================================================
    def _detect_actions(self, text):

        actions = []

        for action, patterns in self.action_patterns.items():

            for pattern in patterns:

                if pattern in text:

                    actions.append(action)
                    break

        return actions

    # ============================================================
    # CONDITION DETECTION
    # ============================================================
    def _detect_conditions(self, text):

        conditions = []

        # ------------------------------------------------
        # SCORE CONDITIONS
        # ------------------------------------------------
        score_patterns = re.findall(
            r"score\s*(>=|<=|>|<|==)\s*(\d+\.?\d*)",
            text
        )

        for operator, value in score_patterns:

            conditions.append({
                "field": "score",
                "operator": operator,
                "value": float(value)
            })

        # ------------------------------------------------
        # CORPORATE EMAIL FILTER
        # ------------------------------------------------
        if "corporate email" in text or "business email" in text:

            conditions.append({
                "field": "email_type",
                "operator": "==",
                "value": "corporate"
            })

        # ------------------------------------------------
        # IGNORE GMAIL
        # ------------------------------------------------
        if "ignore gmail" in text or "exclude gmail" in text:

            conditions.append({
                "field": "email_domain",
                "operator": "!=",
                "value": "gmail.com"
            })

        return conditions