class TaskAgent:
    def __init__(self, name):
        self.name = name
        self.is_base = True  # Se ejecuta siempre primero

    def act(self, state):
        
        data = state.get("data")

        # Simulación simple de procesamiento
        processed = {
            "original": data,
            "status": "processed"
        }

        state.set("processed_data", processed)