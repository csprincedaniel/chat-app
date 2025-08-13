
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from .db import get_db

router = APIRouter()

# response_model makes sure the return value matches 
# the schemas.UserResponse
@router.post("/users/", response_model=schemas.UserResponse)

# get_db() is called before create_user() the returned value from get_db() is 
# passed in through db
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db-db, user=user)