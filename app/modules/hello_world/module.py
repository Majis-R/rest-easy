from fastapi import FastAPI
from .router import router

def register(app: FastAPI) -> None:
    app.include_router(router)