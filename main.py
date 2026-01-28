from typing import Any
from datasets import load_dataset
from elasticsearch import Elasticsearch, helpers

ds = load_dataset("SZTAKI-HLT/HunSum-2-abstractive", split="test")


def main():
    print(f"Number of samples in the test set: {len(ds)}")

    es: Elasticsearch = Elasticsearch("http://localhost:9200")

    if es.indices.exists(index="test-index"):
        es.indices.delete(index="test-index")

    vBody: dict[str, Any] = {
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
            }
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

    if not es.indices.exists(index="test-index"):
        # es.indices.delete(index="test-index")
        es.indices.create(index="test-index", body=vBody)

    helpers.bulk(es, ds, index="test-index")

    result = es.search(
        index="test-index",
        query={"match": {"title": "hír"}},
    )

    print("Got %d Hits:" % result["hits"]["total"]["value"])
    for hit in result["hits"]["hits"]:
        print(hit["_source"]["title"])


# def add(a: Number, b: Number) -> float:
#    return float(a + b)

main()
