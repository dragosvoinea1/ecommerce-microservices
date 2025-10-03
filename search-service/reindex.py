import httpx
import time
from app.es_client import get_es_client
from elasticsearch.helpers import bulk

# Adresele serviciilor definite în docker-compose
PRODUCTS_SERVICE_URL = "http://products-service:8000"
ES_INDEX = "products"

def run_reindex():
    print("--- Script de Re-indexare Elasticsearch ---")
    time.sleep(10) # Așteaptă ca serviciile să pornească

    es = get_es_client()
    if not es:
        print("EROARE: Nu m-am putut conecta la Elasticsearch. Anulare.")
        return

    # 1. Preia TOATE produsele din products-service
    try:
        print(f"Se preiau produsele de la {PRODUCTS_SERVICE_URL}...")
        response = httpx.get(f"{PRODUCTS_SERVICE_URL}/products", timeout=30.0)
        response.raise_for_status()
        products = response.json()
        print(f"S-au găsit {len(products)} produse pentru re-indexare.")
    except Exception as e:
        print(f"EROARE: Nu s-au putut prelua produsele: {e}")
        return

    # 2. Șterge indexul vechi și creează unul nou, gol
    print(f"Se șterge și se recreează index-ul '{ES_INDEX}'...")
    if es.indices.exists(index=ES_INDEX):
        es.indices.delete(index=ES_INDEX)
    es.indices.create(index=ES_INDEX)

    # 3. Indexează în masă (bulk) toate produsele în indexul gol
    actions = []
    for product in products:
        action = {"_index": ES_INDEX, "_id": product["id"], "_source": product}
        actions.append(action)

    if actions:
        print(f"Se importă {len(actions)} documente...")
        try:
            success, _ = bulk(es, actions)
            print(f"✅ Au fost indexate cu succes {success} documente.")
        except Exception as e:
            print(f"EROARE: Importul a eșuat: {e}")
    else:
        print("Niciun produs de indexat.")

    print("--- Re-indexarea s-a finalizat ---")

if __name__ == "__main__":
    run_reindex()