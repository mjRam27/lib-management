import os

from datetime import datetime, timedelta, timezone

import jwt

from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash


load_dotenv()


class AuthService:

    def __init__(self):
        self.password_hasher = PasswordHash.recommended()
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = "HS256"
        self.token_expire_minutes = 30


    def hash_password(
        self,
        password: str
    ) -> str:

        return self.password_hasher.hash(
            password
        )


    def verify_password(
        self,
        password: str,
        password_hash: str
    ) -> bool:

        return self.password_hasher.verify(
            password,
            password_hash
        )

        # return True


    def create_access_token(
        self,
        user_id: int
    ) -> str:

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(
                minutes=self.token_expire_minutes
            )
        )

        payload = {
            "sub": str(user_id),
            "exp": expires_at
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )


    def decode_access_token(
        self,
        token: str
    ) -> int:

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            return int(payload["sub"])

        except (
            InvalidTokenError,
            KeyError,
            ValueError
        ):
            raise ValueError(
                "Invalid or expired token"
            )

