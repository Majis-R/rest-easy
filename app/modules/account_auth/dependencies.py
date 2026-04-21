from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from authlib.jose import jwt

from app.core.secrets import secrets
from app.core.database import get_db
from .services import get_user_by_username
from .models import User

# The tokenUrl must match the route where clients send credentials to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")

def verify_token(token: str) -> dict | None:
    try:
        claims = jwt.decode(token, secrets.SECRET_KEY)
        claims.validate()
        return claims
    except Exception:
        return None

async def auth(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Dependency to retrieve the current authenticated user."""
    claims = verify_token(token)
    
    if not claims or "sub" not in claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = claims["sub"]
    user = await get_user_by_username(db, username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user

async def auth_admin(current_user: User = Depends(auth)) -> User:
    """Dependency to ensure the current authenticated user is an admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough privileges"
        )
    return current_user