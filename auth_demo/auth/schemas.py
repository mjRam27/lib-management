from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(
        from_attributes=True
    )


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str