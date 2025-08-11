from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Register(BaseModel):
    email: str
    password: str

class Login(BaseModel):
    email:str
    password: str

@app.post("/signup")
def signup(request:Register):
   pass 
    