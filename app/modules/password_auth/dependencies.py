from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .services import verify_token

security = HTTPBearer()

def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    claims = verify_token(token)
    if not claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return claims