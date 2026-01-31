from typing import Any, Union
from elasticsearch import Elasticsearch
from fastapi import FastAPI
from adapters.search_backend.search_impl import test

# FastApi teszt
app = FastAPI()


def search_title(query: str) -> list[dict[str, Any]]:
    es: Elasticsearch = Elasticsearch("http://elastic1:9200")
    result = es.search(
        index="test-index",
        query={"match": {"title": query}},
    )
    hits = []
    for hit in result["hits"]["hits"]:
        hits.append(hit["_source"])
    return hits


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/search")
def read_item(q: str) -> dict[str, Union[str, list[dict[str, Any]]]]:
    return {"results": search_title(q)}


@app.get("/test")
def test_call() -> dict[str, str]:
    return {"results": test()}
