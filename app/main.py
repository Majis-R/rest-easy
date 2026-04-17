from fastapi import FastAPI
from app.core.registry import ModuleRegistry
from app.modules.hello_world import module as hello_world_module
from app.modules.password_auth import module as password_auth_module

def create_app() -> FastAPI:
    app = FastAPI(
        title="Rest Easy API",
        description="A secure RESTful API framework template",
        version="0.1.0"
    )

    # Initialize registry
    registry = ModuleRegistry()

    # Explicitly add modules
    registry.add_module(hello_world_module)
    registry.add_module(password_auth_module)

    # Register all modules with the app
    registry.register_all(app)

    return app

app = create_app()