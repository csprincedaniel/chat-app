from fastapi import FastAPI
from backend.db import Base, engine
from . import users

# Creates table
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(users.router)