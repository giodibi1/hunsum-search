from typing import Any, Union
from elasticsearch import Elasticsearch
from fastapi import FastAPI
from pydantic import BaseModel
import adapters.search_backend.search_impl as search_impl
from schemas import document_schema

# FastApi teszt
app = FastAPI()


def search_title(index_name: str, query: str):
    hunsearch = search_impl.HunsumSearchImplementation()
    params: dict[str, Any] = {
        "index": index_name,
        "query": search_impl.HunsumSearchImplementation().search_body(query),
        "size": 10,
        "from_": 0,
    }
    return hunsearch.search(params)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/search")
def read_item(index: str, query: str) -> dict[str, Any]:
    return {"results": search_title(index, query)}


@app.post("/upload_doc/")
async def create_doc(index_name: str, doc: document_schema.Document):
    res = search_impl.HunsumSearchImplementation().upload_doc(
        index_name, doc.model_dump(mode="json")
    )
    if res == False:
        return {"status": "Document upload failed"}
    return doc
