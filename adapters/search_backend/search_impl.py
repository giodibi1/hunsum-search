from typing import Any
from elasticsearch import Elasticsearch, helpers
from dateutil import parser
import re
from .search_interface import *
from datasets import load_dataset


class HunsumSearchImplementation(HunsumSearchInterface):
    es = Elasticsearch("http://elastic1:9200")
    SEARCHFIELDS = ["title", "lead", "article", "date_of_creation"]
    DEFAULTINDEXBODY: dict[str, Any] = {
        "settings": {
            "analysis": {
                "filter": {
                    "hungarian_stop": {"type": "stop", "stopwords": "_hungarian_"},
                    "hungarian_keywords": {
                        "type": "keyword_marker",
                        "keywords": ["példa"],
                    },
                    "hungarian_stemmer": {"type": "stemmer", "language": "hungarian"},
                },
                "analyzer": {
                    "rebuilt_hungarian": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "hungarian_stop",
                            "hungarian_keywords",
                            "hungarian_stemmer",
                        ],
                    }
                },
            },
            "mappings": {
                "properties": {
                    "uuid": {"type": "keyword"},
                    "title": {"type": "text"},
                    "lead": {"type": "text"},
                    "article": {"type": "text"},
                    "domain": {"type": "keyword"},
                    "url": {"type": "text"},
                    "date_of_creation": {
                        "type": "date",
                        "format": "date_optional_time",
                    },
                    "tags": {"type": "keyword"},
                }
            },
        },
        "mappings": {
            "properties": {
                "uuid": {"type": "keyword"},
                "title": {"type": "text", "analyzer": "rebuilt_hungarian"},
                "lead": {"type": "text", "analyzer": "rebuilt_hungarian"},
                "article": {"type": "text", "analyzer": "rebuilt_hungarian"},
                "domain": {"type": "keyword"},
                "url": {"type": "keyword"},
            }
        },
    }

    def init_index(self, name: str, settings: dict = DEFAULTINDEXBODY) -> bool:
        if not self.es.indices.exists(index=name):
            self.es.indices.create(index=name, body=settings)
            ds = load_dataset("SZTAKI-HLT/HunSum-2-abstractive", split="test")
            helpers.bulk(self.es, ds, index=name)
            return True
        return False

    def del_index(self, name: str) -> bool:
        if self.es.indices.exists(index=name):
            self.es.indices.delete(index=name)
            return True
        return False

    def upload_doc(self, index_name: str, doc: document_schema.Document) -> bool:
        res = self.es.index(index=index_name, document=doc)
        return res["result"] == "created" or res["result"] == "updated"

    def date_format_validator(self, date_text: str) -> bool:
        try:
            parser.parse(date_text)
            dateStr: str = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
            return re.search(
                dateStr + "T[0-9]{2}:[0-9]{2}:[0-9]{2}", date_text
            ) or re.search(dateStr, date_text)
        except ValueError:
            return False

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

    def param_sort(self, sort_field: list[str]) -> list[any]:
        sortVar = []
        for s in sort_field:
            field, order = s.split(":")
            if field in self.SEARCHFIELDS and order in ["asc", "desc"]:
                if not any(field in item for item in sortVar):
                    sortVar.append({field: {"order": order}})
            else:
                raise HunsumSearchInterface.SearchFormatException(
                    f"\nInvalid sort option: {s}.\nValid fields: {self.SEARCHFIELDS},\norder: asc, desc",
                    1001,
                )
        return sortVar

    def param_filter(self, filter: list[str]) -> list[dict[str, dict]]:
        filterVar: list[dict[str, dict]] = []
        for f in filter:
            if f.count(":") == 0:
                filterVar.append({"term": {"tags": f}})
            elif f.count(":") == 1:
                val1, val2 = f.split(":")
                if self.date_format_validator(val2):
                    if self.date_format_validator(val1):
                        filterVar.append(
                            {"range": {"date_of_creation": {"gte": val1, "lte": val2}}}
                        )
                    else:
                        raise HunsumSearchInterface.SearchFormatException(
                            f"\nInvalid date format: {val1}",
                            1003,
                        )
                else:
                    if val2 in [
                        "gt",
                        "gte",
                        "lt",
                        "lte",
                    ]:
                        if self.date_format_validator(val1):
                            filterVar.append(
                                {"range": {"date_of_creation": {val2: val1}}}
                            )
                        else:
                            raise HunsumSearchInterface.SearchFormatException(
                                f"\nInvalid date format: {val1}",
                                1003,
                            )
                    else:
                        raise HunsumSearchInterface.SearchFormatException(
                            f"\nInvalid operator format: {val2}.\nValid operators: gt, gte, lt, lte",
                            1003,
                        )
            else:
                raise HunsumSearchInterface.SearchFormatException(
                    f"\nInvalid filter option: {f}.\nToo much parameter.\nOnly two allowed separated by ':'",
                    1002,
                )

        return filterVar

    def search(self, params: dict[str, any]) -> list[dict[str, Any]]:
        result = self.es.search(**params)
        hits = {
            "total": result["hits"]["total"]["value"],
            "pageSize": params["size"],
            "from": params["from_"],
            "hits": [],
        }
        for hit in result["hits"]["hits"]:
            hits["hits"].append(
                {"id": hit["_id"], "score": hit["_score"], **hit["_source"]}
            )
        return hits
