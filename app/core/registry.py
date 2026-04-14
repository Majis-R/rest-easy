# module registration system

from typing import List
from fastapi import FastAPI
from .module_protocol import ModuleProtocol

class ModuleRegistry:
    def __init__(self):
        self.modules: List[ModuleProtocol] = []

    def add_module(self, module: ModuleProtocol) -> None:
        """Explicitly add a module to the registry."""
        self.modules.append(module)

    def register_all(self, app: FastAPI) -> None:
        """Register all added modules with the FastAPI app."""
        for module in self.modules:
            module.register(app)