from typing import Any
from elasticsearch import Elasticsearch
from .search_interface import *


class HunsumSearchImplementation(HunsumSearchInterface):

    def search_body(self, query: str) -> dict[str, Any]:
        query_body = {
            "bool": {
                "must": {
                    "query_string": {
                        "fields": [
                            "tags^4",
                            "title^3",
                            "summary^2",
                            "lead",
                            "article",
                        ],
                        "query": query,
                        "minimum_should_match": 1,
                    }
                }
            }
        }
        return query_body

    def param_page(self, page_number: int = 1, page_size: int = 10) -> dict[str, int]:
        return {"from_": (page_number - 1) * page_size, "size": page_size}

    def param_sort(self, sort_field: list[str], order: str = "desc") -> list[any]:
        pass

    def param_filter(self, filter_field: list[str]) -> list[dict[str, dict]]:
        pass

    def search(self, query: str) -> list[dict[str, Any]]:
        es: Elasticsearch = Elasticsearch("http://localhost:9200")
        result = es.search(
            index="test-index",
            from_=1,
            size=10,
            sort=[{"date_of_creation": {"order": "desc"}}],
            query={
                "bool": {
                    "must": {
                        "query_string": {
                            "fields": [
                                "tags^4",
                                "title^3",
                                "summary^2",
                                "lead",
                                "article",
                            ],
                            "query": query,
                            "minimum_should_match": 1,
                        }
                    },
                    "filter": [
                        # {"term": {"tag": "hír"}},
                        {"range": {"date_of_creation": {"gte": "2020-01-01"}}},
                    ],
                },
                # "query_string": {
                #   "fields": ["tags^4", "title^3", "summary^2", "lead", "article"],
                #  "query": query,
                # "minimum_should_match": 1,
                # },
                # "multi_match": {
                #   "query": query,
                #  "fields": ["tags^4", "title^3", "summary^2", "lead", "article"],
                # },
            },
        )
        hits = []
        for hit in result["hits"]["hits"]:
            hits.append({"id": hit["_id"], "score": hit["_score"], **hit["_source"]})
        return hits


def test():
    return "test"
