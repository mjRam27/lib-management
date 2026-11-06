from fastapi import (
    Depends,
    FastAPI,
    HTTPException
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from sqlalchemy.orm import Session

from auth import AuthService
from database import Base, engine, get_db
from models import User

from schemas import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
    UserUpdate
)

from services import UserService


app = FastAPI(
    title="Authentication CRUD API"
)


Base.metadata.create_all(
    bind=engine
)


auth_service = AuthService()

user_service = UserService()

security = HTTPBearer()


@app.get("/")
def home():

    return {
        "message": "Auth API is running"
    }


@app.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = (
        user_service.get_by_email(
            db,
            data.e
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    password_hash = (
        auth_service.hash_password(
            data.password
        )
    )

    return user_service.create(
        db=db,
        name=data.name,
        email=data.email,
        password_hash=password_hash
    )


@app.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = user_service.get_by_email(
        db,
        data.email
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not auth_service.verify_password(
        data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = (
        auth_service.create_access_token(
            user.id
        )
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_user(
    credentials:
        HTTPAuthorizationCredentials
        = Depends(security),

    db: Session
        = Depends(get_db)

) -> User:

    token = credentials.credentials

    try:

        user_id = (
            auth_service.decode_access_token(
                token
            )
        )

    except ValueError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = user_service.get_by_id(
        db,
        user_id
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@app.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User
        = Depends(get_current_user)
):

    return current_user


@app.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user: User
        = Depends(get_current_user)
):

    return user_service.get_all(db)


@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User
        = Depends(get_current_user)
):

    user = user_service.get_by_id(
        db,
        user_id
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.put(
    "/users/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User
        = Depends(get_current_user)
):

    if current_user.id != user_id:

        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    return user_service.update_name(
        db,
        current_user,
        data.name
    )


@app.delete(
    "/users/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User
        = Depends(get_current_user)
):

    if current_user.id != user_id:

        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    user_service.delete(
        db,
        current_user
    )

    return {
        "message": "User deleted"
    }