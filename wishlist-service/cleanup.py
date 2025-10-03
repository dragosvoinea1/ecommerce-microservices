import os
import httpx
import time
from sqlalchemy import create_engine, select, delete, Table, MetaData, Column, Integer

# Așteaptă puțin pentru a permite celorlalte servicii să pornească complet
time.sleep(5)

# --- Configurare ---
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@wishlist_db/wishlist_db")
PRODUCTS_SERVICE_URL = "http://products-service:8000"

print("--- Script pentru curățarea Wishlist-ului ---")

# --- Conectare la Baza de Date ---
try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Conectat la baza de date a wishlist-ului.")
except Exception as e:
    print(f"❌ EROARE: Nu m-am putut conecta la baza de date: {e}")
    exit()

try:
    # --- Pasul 1: Preia toate ID-urile valide din products-service ---
    print(f"Se preiau ID-urile de produse valide de la {PRODUCTS_SERVICE_URL}...")
    try:
        response = httpx.get(f"{PRODUCTS_SERVICE_URL}/products")
        response.raise_for_status()
        products = response.json()
        valid_product_ids = {product['id'] for product in products}
        print(f"✅ Găsit {len(valid_product_ids)} produse valide.")
    except Exception as e:
        print(f"\n❌ EROARE: Nu s-a putut comunica cu products-service: {e}")
        print("Asigură-te că toate serviciile rulează ('docker-compose up').")
        exit()

    # --- Pasul 2: Preia toate ID-urile din wishlist ---
    meta = MetaData()
    wishlist_items_table = Table('wishlist_items', meta, Column('product_id', Integer))
    
    print("Se preiau ID-urile de produse din wishlist...")
    wishlist_query = select(wishlist_items_table.c.product_id).distinct()
    result = connection.execute(wishlist_query)
    wishlist_product_ids = {row[0] for row in result}
    print(f"✅ Găsit {len(wishlist_product_ids)} ID-uri unice în wishlist.")

    # --- Pasul 3: Identifică ID-urile invalide ("orfane") ---
    orphan_ids = wishlist_product_ids - valid_product_ids
    
    if not orphan_ids:
        print("\n🎉 Nicio intrare invalidă găsită. Wishlist-ul este deja curat!")
    else:
        print(f"\n🟡 Găsit {len(orphan_ids)} ID-uri invalide de șters: {list(orphan_ids)}")

        # --- Pasul 4: Șterge intrările invalide ---
        stmt = delete(wishlist_items_table).where(wishlist_items_table.c.product_id.in_(orphan_ids))
        delete_result = connection.execute(stmt)
        connection.commit() # Folosim commit() pe conexiune în SQLAlchemy 2.0+
        print(f"\n✅ Au fost șterse cu succes {delete_result.rowcount} intrări invalide din wishlist.")

except Exception as e:
    print(f"\n❌ EROARE: A apărut o eroare neașteptată: {e}")
finally:
    connection.close()
    print("\n--- Script finalizat ---")