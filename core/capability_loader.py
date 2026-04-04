import os
import importlib


class CapabilityLoader:

    def __init__(self, registry, base_path="capabilities"):

        self.registry = registry
        self.base_path = base_path

        # 🔧 evita cargas duplicadas
        self.loaded_modules = set()

    # ---------------------------------
    def load(self):

        print("📦 Loading capabilities automatically...")

        # 🔥 Ruta absoluta del proyecto
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # core/ → subir a raíz del proyecto
        project_root = os.path.dirname(current_dir)

        # 📂 Ruta correcta a capabilities
        capabilities_path = os.path.join(project_root, "capabilities")

        print(f"📂 Looking for capabilities in: {capabilities_path}")

        if not os.path.exists(capabilities_path):
            print("❌ Capabilities folder not found")
            return

        for file in os.listdir(capabilities_path):

            # 🔧 ignorar archivos no válidos
            if not file.endswith(".py"):
                continue

            if file.startswith("__"):
                continue

            module_name = file[:-3]

            # 🔧 FIX: evitar cargar módulo dos veces
            if module_name in self.loaded_modules:
                continue

            full_module_path = f"{self.base_path}.{module_name}"

            try:

                module = importlib.import_module(full_module_path)

                capability_instance = None

                # 🔧 buscamos SOLO una clase válida
                for attr_name in dir(module):

                    attr = getattr(module, attr_name)

                    if isinstance(attr, type):

                        try:
                            instance = attr()

                            # 🔧 debe tener método execute
                            if hasattr(instance, "execute"):
                                capability_instance = instance
                                break

                        except Exception:
                            continue

                if capability_instance:

                    if not self.registry.exists(module_name):

                        self.registry.register(
                            module_name,
                            capability_instance
                        )

                        print(f"✅ Loaded capability: {module_name}")

                # marcar como cargado
                self.loaded_modules.add(module_name)

            except Exception as e:

                print(f"❌ Error loading {module_name}: {e}")