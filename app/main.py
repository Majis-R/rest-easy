from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter
from app.core.registry import ModuleRegistry
from app.core.database import engine, Base
from app.core.secrets import secrets
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
    
    # Configure Rate Limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Security Headers Middleware (including HSTS)
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        # HSTS (Strict-Transport-Security)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        # XSS Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    # CORS Middleware
    # Ensure CORS_ORIGINS is a proper list (env may provide JSON string)
    cors_origins = secrets.CORS_ORIGINS
    if isinstance(cors_origins, str):
        try:
            cors_origins = json.loads(cors_origins)
        except Exception:
            cors_origins = [cors_origins]

    # Log the configured origins for debugging
    logging.getLogger("uvicorn").info(f"Configured CORS origins: {cors_origins}")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Small debug middleware: log incoming Origin and whether it's allowed
    @app.middleware("http")
    async def cors_debug(request: Request, call_next):
        origin = request.headers.get("origin")
        if origin:
            allowed = origin in cors_origins or "*" in cors_origins
            logging.getLogger("uvicorn").info(f"CORS check - Origin: {origin}, allowed: {allowed}")
        response = await call_next(request)
        return response

    # Initialize registry
    registry = ModuleRegistry()

    # Explicitly add modules
    # registry.add_module(password_auth_module)
    registry.add_module(account_auth_module)
    registry.add_module(chat_module)

    # Register all modules with the app
    registry.register_all(app)

    @app.get("/test-ui", include_in_schema=False)
    async def test_ui() -> FileResponse:
        return FileResponse(Path(__file__).parent / "web" / "test_ui.html")
        
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Basic health check endpoint."""
        return {"status": "healthy"}

    @app.get("/", include_in_schema=False)
    async def root():
        """Root endpoint that redirects or returns a basic message."""
        return {"message": "Welcome to the API. Access /docs for documentation."}

    return app

app = create_app()