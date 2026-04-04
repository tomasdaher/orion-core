import logging


class IntentParser:
    """
    Intent Parser for Orion.

    Converts natural language user requests into
    structured automation intents.
    """

    def __init__(self):

        self.logger = logging.getLogger("Orion")

        # ------------------------------------------------
        # Goal keywords
        # ------------------------------------------------
        self.goal_keywords = {
            "lead_generation": [
                "lead",
                "leads",
                "clientes potenciales",
                "prospectos"
            ]
        }

        # ------------------------------------------------
        # Source keywords
        # ------------------------------------------------
        self.source_keywords = {
            "instagram": [
                "instagram",
                "ig"
            ],
            "web_form": [
                "formulario",
                "web",
                "landing"
            ],
            "facebook": [
                "facebook",
                "fb"
            ]
        }

        # ------------------------------------------------
        # Action keywords
        # ------------------------------------------------
        self.action_keywords = {
            "capture": [
                "capturar",
                "capture",
                "obtener",
                "extraer"
            ],
            "clean": [
                "limpiar",
                "clean",
                "normalizar"
            ],
            "classify": [
                "clasificar",
                "classify",
                "segmentar"
            ],
            "store": [
                "guardar",
                "store",
                "almacenar"
            ],
            "notify": [
                "notificar",
                "avisar",
                "alertar"
            ]
        }

    # ------------------------------------------------
    # Parse main entrypoint
    # ------------------------------------------------
    def parse(self, text):

        self.logger.info(f"🧠 Parsing user intent: {text}")

        text = text.lower()

        intent = {
            "goal": self.detect_goal(text),
            "source": self.detect_source(text),
            "actions": self.detect_actions(text)
        }

        self.logger.info(f"🎯 Structured intent detected: {intent}")

        return intent

    # ------------------------------------------------
    # Detect goal
    # ------------------------------------------------
    def detect_goal(self, text):

        for goal, keywords in self.goal_keywords.items():

            for keyword in keywords:

                if keyword in text:
                    return goal

        return None

    # ------------------------------------------------
    # Detect source
    # ------------------------------------------------
    def detect_source(self, text):

        for source, keywords in self.source_keywords.items():

            for keyword in keywords:

                if keyword in text:
                    return source

        return None

    # ------------------------------------------------
    # Detect actions
    # ------------------------------------------------
    def detect_actions(self, text):

        detected = []

        for action, keywords in self.action_keywords.items():

            for keyword in keywords:

                if keyword in text:
                    detected.append(action)
                    break

        # Default automation pipeline
        if not detected:
            detected = [
                "capture",
                "clean",
                "classify",
                "store",
                "notify"
            ]

        return detected