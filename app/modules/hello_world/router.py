from fastapi import APIRouter, Depends

router = APIRouter(prefix="/hello", tags=["Hello World"])

@router.get("/")
async def hello_world():
    return {"message": "Hello, World! This is the Hello World module."}