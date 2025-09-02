from fastapi import FastAPI, Depends
from elasticsearch import Elasticsearch
from .es_client import get_es_client

app = FastAPI(title="Search Service")

@app.get("/search")
def search_products(q: str, es: Elasticsearch = Depends(get_es_client)):
    if not q:
        return []

    # Construim o interogare "boolean" care combină mai multe tipuri de căutări
    query = {
        "size": 10,
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": q,
                            "fields": ["name", "description"],
                            "type": "best_fields",
                            "fuzziness": "AUTO"
                        }
                    },
                    {
                        "multi_match": {
                            "query": q,
                            "fields": ["name", "description"],
                            "type": "phrase_prefix"
                        }
                    }
                ]
            }
        }
    }

    try:
        response = es.search(index="products", body=query)
        return [hit['_source'] for hit in response['hits']['hits']]
    except Exception as e:
        # Într-o aplicație reală, am loga eroarea mai detaliat
        print(f"Error during search: {e}")
        return {"error": "Search failed"}
    

