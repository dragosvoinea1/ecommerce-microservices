import pika
import json
import os
import time
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from .models import DBWishlistItem

print(' [WISHLIST CONSUMER] Script started.')
time.sleep(15) 

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

RABBITMQ_URL = os.environ.get("RABBITMQ_URL")
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
channel = connection.channel()

# --- MODIFICĂRI AICI ---
# 1. Declară exchange-ul
channel.exchange_declare(exchange='product_events_exchange', exchange_type='fanout')

# 2. Creează o coadă temporară și exclusivă
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 3. Leagă coada la exchange
channel.queue_bind(exchange='product_events_exchange', queue=queue_name)


def callback(ch, method, properties, body):
    """Procesează un mesaj primit de la coada de evenimente."""
    print(f" [WISHLIST CONSUMER] Received {body.decode()}")
    data = json.loads(body)
    
    action = data.get('action')
    product = data.get('product')

    if action == 'delete':
        product_id = product.get('id')
        if not product_id:
            ch.basic_ack(delivery_tag=method.delivery_tag) # Confirmă mesajele pe care le ignoră
            return

        db = SessionLocal()
        try:
            stmt = delete(DBWishlistItem).where(DBWishlistItem.product_id == product_id)
            result = db.execute(stmt)
            db.commit()
            print(f"  - Deleted {result.rowcount} wishlist item(s) for product ID {product_id}.")
        except Exception as e:
            print(f"Error processing delete event: {e}")
            db.rollback()
        finally:
            db.close()
    
    # 4. Confirmă manual mesajul, indiferent dacă a fost procesat sau ignorat
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 5. Consumă din coada nouă, cu auto_ack=False
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

print(f' [WISHLIST CONSUMER] Waiting for product events on queue "{queue_name}"...')
channel.start_consuming()