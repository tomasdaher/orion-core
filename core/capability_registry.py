import os
import importlib
import inspect
import logging
import sys
import re

class CapabilityRegistry:

    def __init__(self, plugins_path="plugins"):

        self.logger = logging.getLogger("Orion")

        self.plugins_path = plugins_path

        self.capabilities = {}

        # 🔥 referencia al engine (clave en esta etapa)
        self.capability_engine = None

        self._ensure_plugins_package()

    # ------------------------------------------------
    # Ensure plugins folder exists and is importable
    # ------------------------------------------------
    def _ensure_plugins_package(self):

        if not os.path.exists(self.plugins_path):

            os.makedirs(self.plugins_path)

            self.logger.info(
                f"📁 Created plugins directory: {self.plugins_path}"
            )

        init_file = os.path.join(self.plugins_path, "__init__.py")

        if not os.path.exists(init_file):

            open(init_file, "w").close()

    # ------------------------------------------------
    # 🔥 LOAD INTO ENGINE
    # ------------------------------------------------
    def load(self, capability_engine):

        self.logger.info("📦 Loading capabilities into engine...")

        self.capability_engine = capability_engine

        self.capabilities = {}

        importlib.invalidate_caches()

        loaded = []

        for filename in os.listdir(self.plugins_path):

            if not filename.endswith(".py"):
                continue

            if filename.startswith("__"):
                continue

            module_name = filename[:-3]
            module_path = f"{self.plugins_path}.{module_name}"

            try:

                # 🔥 evitar cache
                if module_path in sys.modules:
                    del sys.modules[module_path]

                module = importlib.import_module(module_path)

                registered = self._register_module_capabilities(module)

                loaded.extend(registered)

            except Exception as e:

                self.logger.warning(
                    f"⚠️ Failed loading module {module_name}: {e}"
                )

        self.logger.info(
            f"📦 Total capabilities loaded: {len(loaded)}"
        )

        return loaded

    # ------------------------------------------------
    # Register capability classes
    # ------------------------------------------------
    def _register_module_capabilities(self, module):

        registered = []

        for name, obj in inspect.getmembers(module):

            if inspect.isclass(obj) and hasattr(obj, "execute"):

                try:

                    instance = obj()

                    capability_name = getattr(
                        instance,
                        "name",
                        name.lower()
                    )

                    if capability_name in self.capabilities:

                        self.logger.info(
                            f"♻️ Skipping duplicate: {capability_name}"
                        )
                        continue

                    self.capabilities[capability_name] = instance

                    # 🔥 registrar también en el engine
                    if self.capability_engine:

                        self.capability_engine.register_capability(
                            capability_name,
                            instance
                        )

                    registered.append(capability_name)

                    self.logger.info(
                        f"✅ Capability registered: {capability_name}"
                    )

                except Exception as e:

                    self.logger.warning(
                        f"⚠️ Failed instantiating {name}: {e}"
                    )

        return registered

    # ------------------------------------------------
    # 🔥 FIX CLAVE → GET (COMPATIBLE CON ORCHESTRATOR)
    # ------------------------------------------------
    def get(self, name):
        return self.capabilities.get(name)

    # ------------------------------------------------
    def get_capability(self, name):
        return self.capabilities.get(name)

    # ------------------------------------------------
    def has_capability(self, name):
        return name in self.capabilities

    # ------------------------------------------------
    def execute(self, name, state):

        capability = self.get_capability(name)

        if not capability:
            raise Exception(f"Capability not found: {name}")

        self.logger.info(f"⚙️ Executing capability: {name}")

        return capability.execute(state)

    # ------------------------------------------------
    
    def register(self, name, capability):

        # 🔧 Normalizar nombre a snake_case
        normalized_name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

        # Prevent duplicate registrations
        if normalized_name in self.capabilities:

            if self.logger:
                self.logger.debug(
                    f"⚠️ Capability already registered, skipping: {normalized_name}"
                )

            return

        self.capabilities[normalized_name] = capability

        # 🔥 sync con engine
        if self.capability_engine:

            self.capability_engine.register_capability(
                normalized_name,
                capability
            )

        if self.logger:
            self.logger.info(
                f"📦 Capability manually registered: {normalized_name}"
            )

    # ------------------------------------------------
    def exists(self, name):
        return name in self.capabilities

    # ------------------------------------------------
    # 🔥 RELOAD REAL (MEJORADO)
    # ------------------------------------------------
    def reload(self):

        self.logger.info("♻️ Reloading capabilities (full refresh)")

        if self.capability_engine:
            try:
                self.capability_engine.clear()
            except Exception:
                pass

        self.capabilities = {}

        importlib.invalidate_caches()

        # limpiar módulos
        for module_name in list(sys.modules.keys()):

            if module_name.startswith(self.plugins_path):
                del sys.modules[module_name]

        # 🔥 volver a cargar en engine
        if self.capability_engine:
            self.load(self.capability_engine)
        else:
            self.load(None)

        self.logger.info(
            f"🚀 Reload complete: {len(self.capabilities)} capabilities active"
        )

    # ------------------------------------------------
    def list_capabilities(self):
        return list(self.capabilities.keys())