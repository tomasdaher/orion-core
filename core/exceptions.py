class OrionCoreException(Exception):
    """Excepción base del sistema Orion Core."""
    pass


class AgentExecutionError(OrionCoreException):
    """Error durante ejecución de un agente."""
    pass


class RuleEvaluationError(OrionCoreException):
    """Error durante evaluación de una regla."""
    pass