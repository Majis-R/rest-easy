import time
from authlib.jose import jwt
from app.core.secrets import secrets

ALGORITHM = "HS256"

def authenticate(password: str) -> bool:
    return password == secrets.set_password

def create_access_token() -> str:
    header = {"alg": ALGORITHM}
    payload = {
        "sub": "admin",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600 # 1 hour expiration
    }
    return jwt.encode(header, payload, secrets.secret_key).decode('utf-8')

def verify_token(token: str) -> dict:
    try:
        claims = jwt.decode(token, secrets.secret_key)
        claims.validate()
        return claims
    except Exception:
        return None