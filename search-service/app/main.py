import os
from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI(title="Search Service")

ES_HOST = os.environ.get("ELASTICSEARCH_HOST")
es = Elasticsearch([{'host': ES_HOST, 'port': 9200, 'scheme': 'http'}])

@app.get("/search")
def search_products(q: str):
    """Caută produse în Elasticsearch."""
    if not q:
        return []

    # Construim o interogare avansată (fuzzy search)
    query = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["name", "description"],
                "fuzziness": "AUTO"
            }
        }
    }

    try:
        response = es.search(index="products", body=query)
        # Extragem doar documentele sursă din răspuns
        return [hit['_source'] for hit in response['hits']['hits']]
    except Exception as e:
        return {"error": str(e)}