from datasets import load_dataset
from elasticsearch import Elasticsearch

ds = load_dataset("SZTAKI-HLT/HunSum-2-abstractive", split="test")


def main():
    print("Hello from hunsum-search! Commit test")
    print(f"Number of samples in the test set: {len(ds)}")
    es = Elasticsearch("http://localhost:9200")
    print(es.info())


# def add(a: Number, b: Number) -> float:
#    return float(a + b)

main()
