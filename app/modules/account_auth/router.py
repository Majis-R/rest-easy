import time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from authlib.jose import jwt

from app.core.database import get_db
from app.core.secrets import secrets
from .schemas import UserCreate, UserResponse, TokenResponse
from .services import get_user_by_username, create_user, verify_password, get_all_users, delete_user
from .dependencies import auth_admin
from .models import User

router = APIRouter(prefix="/account", tags=["Account Auth"])

def create_access_token(username: str, role: str) -> str:
    """Generate a JWT for the authenticated user."""
    header = {"alg": "HS256"}
    payload = {
        "sub": username,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }
    return jwt.encode(header, payload, secrets.SECRET_KEY).decode('utf-8')

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    new_user = await create_user(db, user)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Authenticate a user and return a JWT following OAuth2 spec."""
    db_user = await get_user_by_username(db, form_data.username)
    
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(db_user.username, db_user.role)
    return TokenResponse(access_token=token, token_type="bearer")


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(auth_admin)
):
    """List all accounts (Admin only)."""
    return await get_all_users(db)

@router.delete("/delete/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
    username: str,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(auth_admin)
):
    """Delete an account (Admin only)."""
    success = await delete_user(db, username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None