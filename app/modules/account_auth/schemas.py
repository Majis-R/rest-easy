from pydantic import BaseModel, Field

# Input schema for registration and login
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    #TODO Increase min_length and add regex for password complexity in a real application
    password: str = Field(..., min_length=3)  

# Output schema (hides the password)
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True # Allows Pydantic to read from SQLAlchemy ORM models

# Token response (same as simple auth)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"