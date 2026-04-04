from core.orchestrator import Orchestrator
from core.execution_request import Objective
from core.registry import AgentRegistry
from core.memory_service import MemoryService
from core.capability_registry import CapabilityRegistry
from core.capability_loader import CapabilityLoader
from core.goal_engine import GoalEngine

from infrastructure.repositories.sqlite_execution_repository import SQLiteExecutionRepository
from infrastructure.database import Database

from integrations.integration_manager import IntegrationManager
from integrations.api_connector import APIConnector
from integrations.database_connector import DatabaseConnector
from integrations.webhook_connector import WebhookConnector


def build_system():

    # ---------------------------------
    # DATABASE
    # ---------------------------------
    db = Database()
    db.initialize()

    # ---------------------------------
    # INFRASTRUCTURE
    # ---------------------------------
    repository = SQLiteExecutionRepository()
    memory_service = MemoryService(repository)

    # ---------------------------------
    # 🔥 CAPABILITY SYSTEM
    # ---------------------------------
    capability_registry = CapabilityRegistry()

    capability_loader = CapabilityLoader(capability_registry)
    capability_loader.load()

    # ---------------------------------
    # INTEGRATIONS
    # ---------------------------------
    integration_manager = IntegrationManager()

    integration_manager.register_connector_type("api", APIConnector)
    integration_manager.register_connector_type("database", DatabaseConnector)
    integration_manager.register_connector_type("webhook", WebhookConnector)

    integration_manager.initialize_connector(
        "webhook",
        {"url": "https://httpbin.org/post"}
    )

    integration_manager.initialize_connector(
        "api",
        {"base_url": "https://jsonplaceholder.typicode.com"}
    )

    # ---------------------------------
    # 🧠 GOAL ENGINE
    # ---------------------------------
    goal_engine = GoalEngine(
        memory=memory_service,
        planner=None  # se conectará con PlanningAgent después
    )

    # ---------------------------------
    # CORE
    # ---------------------------------
    orchestrator = Orchestrator(
        repository=repository,
        memory_service=memory_service,
        capability_registry=capability_registry,
    )

    # ---------------------------------
    # AGENTS
    # ---------------------------------
    registry = AgentRegistry(
        dependencies={
            "memory_service": memory_service,
            "integration_manager": integration_manager,
            "capability_registry": capability_registry
        }
    )

    registry.discover_and_register()

    for agent in registry.all().values():

        orchestrator.register_agent(agent)

        # conectar PlanningAgent con GoalEngine
        if agent.__class__.__name__ == "PlanningAgent":

            goal_engine.planner = agent

    return orchestrator