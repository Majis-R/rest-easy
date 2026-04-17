from fastapi import APIRouter, Depends
from app.modules.password_auth.dependencies import require_auth

router = APIRouter(prefix="/hello", tags=["Hello World"])

@router.get("/", dependencies=[Depends(require_auth)])
async def hello_world():
    return {"message": "Hello, World! This is the Hello World module."}