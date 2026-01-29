from typing import Union
from fastapi import FastAPI
from main import search_title

# FastApi teszt
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
def read_item(q: str):
    return {"results": q}


# @app.get("/search")
# def read_item(q: str):
#    return search_title(q)
