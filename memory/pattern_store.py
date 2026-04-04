import json
import os


class PatternStore:

    def __init__(self, filepath="memory/pattern_memory.json"):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        """
        Asegura que el archivo de memoria exista.
        Si no existe, lo crea con la estructura inicial.
        """

        if not os.path.exists(self.filepath):

            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

            initial_data = {
                "patterns": {}
            }

            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

    def load(self):
        """
        Carga los patrones almacenados.
        """

        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        """
        Guarda patrones en memoria persistente.
        """

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def increment_pattern(self, signature):
        """
        Incrementa la frecuencia de un patrón observado.
        """

        data = self.load()

        patterns = data.get("patterns", {})

        patterns[signature] = patterns.get(signature, 0) + 1

        data["patterns"] = patterns

        self.save(data)

    def get_patterns(self):
        """
        Devuelve todos los patrones registrados.
        """

        data = self.load()
        return data.get("patterns", {})