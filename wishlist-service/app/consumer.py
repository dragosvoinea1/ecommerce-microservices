import pika
import json
import os
import time
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from .models import DBWishlistItem

print(' [WISHLIST CONSUMER] Script started. Waiting for messages.')

# Așteptăm ca baza de date să fie gata
time.sleep(15) 

# Conexiunea la Baza de Date
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Conexiunea la RabbitMQ
RABBITMQ_URL = os.environ.get("RABBITMQ_URL")
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
channel = connection.channel()

# Ne conectăm la aceeași coadă pe care o folosește și search-service
channel.queue_declare(queue='product_events_queue', durable=True)

def callback(ch, method, properties, body):
    """Procesează un mesaj primit de la coada de evenimente."""
    print(f" [WISHLIST CONSUMER] Received {body.decode()}")
    data = json.loads(body)
    
    action = data.get('action')
    product = data.get('product')

    # Ne interesează doar evenimentele de ștergere
    if action == 'delete':
        product_id = product.get('id')
        if not product_id:
            return

        db = SessionLocal()
        try:
            # Construim și executăm comanda de ștergere
            stmt = delete(DBWishlistItem).where(DBWishlistItem.product_id == product_id)
            result = db.execute(stmt)
            db.commit()
            print(f"  - Deleted {result.rowcount} wishlist item(s) for product ID {product_id}.")
        except Exception as e:
            print(f"Error processing delete event: {e}")
            db.rollback()
        finally:
            db.close()

channel.basic_consume(queue='product_events_queue', on_message_callback=callback, auto_ack=True)

print(' [WISHLIST CONSUMER] Waiting for product events...')
channel.start_consuming()