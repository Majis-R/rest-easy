from fastapi import APIRouter, HTTPException, status
from .schemas import LoginRequest, TokenResponse
from .services import authenticate, create_access_token

router = APIRouter(prefix="/auth", tags=["Simple Auth"])

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    if not authenticate(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    return TokenResponse(access_token=create_access_token(), token_type="bearer")