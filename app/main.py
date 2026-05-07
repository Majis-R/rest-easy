from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.core.registry import ModuleRegistry
from app.core.database import engine, Base
from app.modules.hello_world import module as hello_world_module
from app.modules.password_auth import module as password_auth_module
from app.modules.account_auth import module as account_auth_module
from app.modules.chat_module import module as chat_module

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables in the DB
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Clean up engine
    await engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Rest Easy API",
        description="A secure RESTful API template",
        version="0.1.0",
        lifespan=lifespan
    )

    # Initialize registry
    registry = ModuleRegistry()

    # Explicitly add modules
    registry.add_module(hello_world_module)
    # registry.add_module(password_auth_module)
    registry.add_module(account_auth_module)
    registry.add_module(chat_module)

    # Register all modules with the app
    registry.register_all(app)

    @app.get("/test-ui", include_in_schema=False)
    async def test_ui() -> FileResponse:
        return FileResponse(Path(__file__).parent / "web" / "test_ui.html")

    return app

app = create_app()