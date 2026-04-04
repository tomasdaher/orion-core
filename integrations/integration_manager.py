import logging
from typing import Dict, Type, Optional
from integrations.base_connector import BaseConnector


class IntegrationManager:

    def __init__(self):

        self.logger = logging.getLogger("Orion.Integrations")

        # nombre → instancia del conector
        self._connectors: Dict[str, BaseConnector] = {}

        # nombre → clase del conector
        self._connector_types: Dict[str, Type[BaseConnector]] = {}

    # ---------------------------------
    # REGISTER CONNECTOR TYPE
    # ---------------------------------

    def register_connector_type(
        self,
        name: str,
        connector_class: Type[BaseConnector]
    ):

        if not issubclass(connector_class, BaseConnector):
            raise ValueError(
                f"{connector_class} must inherit from BaseConnector"
            )

        self._connector_types[name] = connector_class

        self.logger.info(
            f"Connector type registered: {name}"
        )

    # ---------------------------------
    # INITIALIZE CONNECTOR INSTANCE
    # ---------------------------------

    def initialize_connector(
        self,
        name: str,
        config: Optional[dict] = None
    ):

        connector_class = self._connector_types.get(name)

        if not connector_class:
            raise ValueError(
                f"Connector type not registered: {name}"
            )

        connector = connector_class(config)

        connector.connect()

        self._connectors[name] = connector

        self.logger.info(
            f"Connector initialized: {name}"
        )

    # ---------------------------------
    # GET CONNECTOR
    # ---------------------------------

    def get_connector(self, name: str) -> BaseConnector:

        connector = self._connectors.get(name)

        if not connector:
            raise ValueError(
                f"Connector not initialized: {name}"
            )

        return connector

    # ---------------------------------
    # EXECUTE ACTION THROUGH CONNECTOR
    # ---------------------------------

    def execute(
        self,
        connector_name: str,
        action: str,
        payload: Optional[dict] = None
    ):

        connector = self.get_connector(connector_name)

        try:

            result = connector.execute(action, payload)

            self.logger.info(
                f"Connector action executed: "
                f"{connector_name}.{action}"
            )

            return result

        except Exception as e:

            self.logger.error(
                f"Connector execution failed: "
                f"{connector_name}.{action} | {str(e)}"
            )

            raise

    # ---------------------------------
    # LIST CONNECTORS
    # ---------------------------------

    def list_connectors(self):

        return list(self._connectors.keys())

    # ---------------------------------
    # HEALTH CHECK
    # ---------------------------------

    def health_check(self):

        status = {}

        for name, connector in self._connectors.items():

            try:

                connector.connect()

                status[name] = "healthy"

            except Exception:

                status[name] = "error"

        return status