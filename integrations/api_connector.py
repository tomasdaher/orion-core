import requests
from integrations.base_connector import BaseConnector


class APIConnector(BaseConnector):

    name = "APIConnector"

    def connect(self):

        self.base_url = self.config.get("base_url")

        if not self.base_url:
            raise ValueError("API base_url not provided")

    def read(self, endpoint):

        url = f"{self.base_url}/{endpoint}"

        response = requests.get(url)

        return self._parse_response(response)

    def write(self, endpoint, data):

        url = f"{self.base_url}/{endpoint}"

        response = requests.post(url, json=data)

        return self._parse_response(response)

    def execute(self, action, payload=None):

        return self.write(action, payload)

    # ---------------------------------
    # RESPONSE PARSER
    # ---------------------------------

    def _parse_response(self, response):

        try:
            return response.json()

        except Exception:

            return {
                "status_code": response.status_code,
                "response_text": response.text
            }