# search-service/app/main.py
from fastapi import FastAPI, Depends
from elasticsearch import Elasticsearch
from .es_client import get_es_client

app = FastAPI(title="Search Service")

@app.get("/search")
def search_products(q: str, es: Elasticsearch = Depends(get_es_client)):
    if not q: return []
    
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
        return [hit['_source'] for hit in response['hits']['hits']]
    except Exception as e:
        return {"error": str(e)}