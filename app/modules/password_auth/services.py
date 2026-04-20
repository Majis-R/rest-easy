import time
from authlib.jose import jwt
from app.core.secrets import secrets

ALGORITHM = "HS256"

def authenticate(password: str) -> bool:
    return password == secrets.COMMON_PASSWORD

def create_access_token() -> str:
    header = {"alg": ALGORITHM}
    payload = {
        "sub": "admin",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600 # 1 hour expiration
    }
    return jwt.encode(header, payload, secrets.SECRET_KEY).decode('utf-8')

def verify_token(token: str) -> dict:
    try:
        claims = jwt.decode(token, secrets.SECRET_KEY)
        claims.validate()
        return claims
    except Exception:
        return None