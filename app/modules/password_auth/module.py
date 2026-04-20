# This module implements a simple password-based authentication system. 
# It includes a single hardcoded password that clients must provide 
# to access protected routes. The module uses JWT tokens to manage 
# authentication state, and it provides a dependency that can be used 
# to protect routes with this authentication mechanism.
from fastapi import FastAPI
from .router import router

def register(app: FastAPI) -> None:
    app.include_router(router)