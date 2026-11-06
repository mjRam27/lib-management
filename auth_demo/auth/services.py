from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User


class UserService:

    def get_all(
        self,
        db: Session
    ) -> list[User]:

        statement = select(User)

        users = db.scalars(
            statement
        ).all()

        return list(users)


    def get_by_id(
        self,
        db: Session,
        user_id: int
    ) -> User | None:

        return db.get(
            User,
            user_id
        )


    def get_by_email(
        self,
        db: Session,
        email: str
    ) -> User | None:

        statement = select(User).where(
            User.email == email
        )

        return db.scalar(statement)


    def create(
        self,
        db: Session,
        name: str,
        email: str,
        password_hash: str
    ) -> User:

        user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return user


    def update_name(
        self,
        db: Session,
        user: User,
        name: str
    ) -> User:

        user.name = name

        db.commit()

        db.refresh(user)

        return user


    def delete(
        self,
        db: Session,
        user: User
    ) -> None:

        db.delete(user)

        db.commit()