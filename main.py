from enum import Enum
from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel
from typing import Dict, List


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return {"message": "Welcome to the root endpoint"}



@app.get("/post", response_model=List[Timestamp])
def get_posts():
    return post_db

@app.get("/dog", response_model=List[Dog])
def get_dogs(kind: DogType = Query(None, description="Filter by dog kind")):
    if kind:
        filtered_dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
        return filtered_dogs
    return list(dogs_db.values())

@app.get("/dog/{pk}", response_model=Dog)
def get_dog_by_pk(pk: int = Path(..., description="Primary Key (pk) of the dog")):
    if pk in dogs_db:
        return dogs_db[pk]
    else:
        raise HTTPException(status_code=404, detail="Dog not found")

@app.post("/dog", response_model=Dog)
def create_dog(dog: Dog = Body(..., description="Dog data to create")):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=400, detail="Dog with the same pk already exists")
    dogs_db[dog.pk] = dog
    return dog

@app.patch("/dog/{pk}", response_model=Dog)
def update_dog(pk: int = Path(..., description="Primary Key (pk) of the dog"), updated_dog: Dog = Body(..., description="Updated dog data")):
    if pk in dogs_db:
        dogs_db[pk] = updated_dog
        return updated_dog
    else:
        raise HTTPException(status_code=404, detail="Dog not found")
