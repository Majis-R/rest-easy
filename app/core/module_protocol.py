from typing import Protocol
from fastapi import FastAPI

class ModuleProtocol(Protocol):
    def register(self, app: FastAPI) -> None:
        ...