from state.state_manager import StateManager
from core.logger import setup_logger
from core.rule_engine import Rule



class Orchestrator:
    def __init__(self, repository):
        self.logger = setup_logger()
        self.agents = {}
        self.rules = []
        self.state = StateManager()
        self.repository = repository

    def add_agent(self, agent):
        self.logger.info(f"Agente registrado: {agent.name}")
        self.agents[agent.name] = agent

    def add_rule(self, rule):
        self.logger.info(f"Regla agregada para: {rule.action_agent_name}")
        self.rules.append(rule)

    def execute(self, request):
        execution_status = "SUCCESS"

        try:
            self.logger.info(f"Nuevo request recibido: {request.objective}")

            self.state.set("objective", request.objective)
            self.state.set("data", request.data)
            self.state.set("execution_id", request.execution_id)

            # Ejecutar agentes base
            for agent in self.agents.values():
                if hasattr(agent, "is_base") and agent.is_base:
                    self.logger.info(f"Ejecutando agente base: {agent.name}")
                    try:
                        agent.act(self.state)
                    except Exception as e:
                        execution_status = "FAILED"
                        self.logger.error(f"Error en agente {agent.name}: {str(e)}")
                        raise

            # Evaluar reglas
            for rule in self.rules:
                try:
                    if rule.evaluate(self.state):
                        agent_name = rule.action_agent_name
                        if agent_name in self.agents:
                            self.logger.info(f"Regla cumplida → Ejecutando {agent_name}")
                            self.agents[agent_name].act(self.state)
                except Exception as e:
                    execution_status = "FAILED"
                    self.logger.error(f"Error evaluando regla: {str(e)}")
                    raise

        except Exception as e:
            execution_status = "FAILED"
            self.logger.error(f"Ejecución interrumpida: {str(e)}")

        finally:
            self.state.set("execution_status", execution_status)
            
            # Aqui va la persistencia
            filepath = self.repository.save(request, self.state)
            self.logger.info(f"Ejecución guardada en: {filepath}")

            self.logger.info(f"Estado final: {self.state.get_all()}")
            self.logger.info("Ejecución completada")