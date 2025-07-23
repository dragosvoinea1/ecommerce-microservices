import pika
import json
import os
import time
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from .models import DBProduct

print(' [*] Consumer script started. Waiting for messages.')

# Așteptăm ca baza de date să fie gata
time.sleep(10) 

# Conexiunea la Baza de Date
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Conexiunea la RabbitMQ
RABBITMQ_URL = os.environ.get("RABBITMQ_URL")
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
channel = connection.channel()
channel.queue_declare(queue='stock_update_queue')

def callback(ch, method, properties, body):
    """Funcția care procesează un mesaj primit."""
    print(f" [x] Received {body.decode()}")
    data = json.loads(body)
    
    db = SessionLocal()
    try:
        for product_data in data.get('products', []):
            product_id = product_data.get('product_id')
            quantity_sold = product_data.get('quantity')
            
            # Găsim produsul în baza de date
            product_to_update = db.query(DBProduct).filter(DBProduct.id == product_id).first()
            
            if product_to_update:
                # Scădem stocul
                new_stock = product_to_update.stock - quantity_sold
                product_to_update.stock = new_stock
                print(f"  - Updated stock for product {product_id} to {new_stock}")
        
        db.commit()
        print(" [x] Done processing message.")
    except Exception as e:
        print(f"Error processing message: {e}")
        db.rollback()
    finally:
        db.close()

channel.basic_consume(queue='stock_update_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()