"""
User Segmenter Capability

Clasifica usuarios en segmentos según su score.
Esto permite que Orion tome decisiones más inteligentes
en base al valor del usuario.
"""


class UserSegmenter:

    def __init__(self):
        self.name = "user_segmenter"

    def execute(self, state):

        # ---------------------------------
        # Obtener usuario desde el estado
        # ---------------------------------

        user = state.get("user")

        if not user:
            print("⚠️ No user found in state")
            return {
                "capability": self.name,
                "status": "no_user"
            }

        score = user.get("score", 0)

        print(f"🧠 Evaluating user score: {score}")

        # ---------------------------------
        # Lógica de segmentación
        # ---------------------------------

        if score >= 20:
            segment = "premium"
        elif score >= 10:
            segment = "warm"
        else:
            segment = "cold"

        print(f"🎯 User segment: {segment}")

        # ---------------------------------
        # Guardar en el estado global
        # ---------------------------------

        state["user_segment"] = segment
        state["last_capability"] = self.name

        # ---------------------------------
        # Resultado
        # ---------------------------------

        return {
            "capability": self.name,
            "status": "segmented",
            "segment": segment,
            "score": score
        }