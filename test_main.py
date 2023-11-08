from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/say_hello")
def read_root():
    return "Hello"

@app.get("/")
def root():
    return {"Hello":"world"}