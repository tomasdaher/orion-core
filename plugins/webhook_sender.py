import requests


class WebhookSender:

    def __init__(self):
        # ⚠️ Debe coincidir EXACTAMENTE con el workflow
        self.name = "webhook_sender"

    def execute(self, state):

        data = state.get("data", {})

        # URL dinámica (puede venir del evento)
        url = data.get("webhook_url", "https://httpbin.org/post")

        payload = {
            "event": "new_customer",
            "data": data
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=5
            )

            result = {
                "status": "success",
                "status_code": response.status_code,
                "response": response.text[:200]  # limitamos tamaño
            }

        except Exception as e:
            result = {
                "status": "error",
                "error": str(e)
            }

        # tracking interno de Orion
        state["last_capability"] = self.name

        return result