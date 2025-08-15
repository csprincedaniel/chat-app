from sqlalchemy.orm import Session
from . import models, schemas
from passlib.hash import bcrypt


def create_user(db:Session, user: schemas.UserCreate):
    hashed_pw = bcrypt.hash(user.password)

    db_user = models.Users(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )

    db.add(db_user)
    db.commit()

    # Reloads the database generated values like an id
    db.refresh(db_user) 

    return db_user
