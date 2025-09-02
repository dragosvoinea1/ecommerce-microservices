# search-service/app/es_client.py
from elasticsearch import Elasticsearch
import os
import time

es_client = None

def get_es_client():
    global es_client
    if es_client is None:
        print(" [ES_CLIENT] No existing client, attempting to connect...")
        es_url = os.environ.get("ELASTICSEARCH_URL")
        retries = 30
        while retries > 0:
            try:
                client = Elasticsearch(es_url)
                if client.ping():
                    print(" [ES_CLIENT] Elasticsearch connection successful.")
                    es_client = client
                    break
                else:
                    raise ConnectionError("Ping failed")
            except Exception as e:
                print(f" [!] ES not available (error: {e}), retrying... ({retries})")
                time.sleep(5)
                retries -= 1
        if es_client is None:
            raise ConnectionError("Could not connect to Elasticsearch after multiple retries.")
    return es_client