import requests
from integrations.base_connector import BaseConnector


class WebhookConnector(BaseConnector):

    name = "WebhookConnector"

    def connect(self):

        self.webhook_url = self.config.get("url")

        if not self.webhook_url:
            raise ValueError("Webhook URL missing")

    def read(self, query=None):

        return None

    def write(self, data):

        response = requests.post(self.webhook_url, json=data)

        return response.status_code

    def execute(self, action, payload=None):

        return self.write(payload)