from typing import Any
from elasticsearch import Elasticsearch


def search_title(query: str) -> list[dict[str, Any]]:
    es: Elasticsearch = Elasticsearch("http://localhost:9200")
    result = es.search(
        index="test-index",
        query={"match": {"title": query}},
    )
    hits = []
    for hit in result["hits"]["hits"]:
        hits.append(hit["_source"])
    return hits


def test():
    return "test"
