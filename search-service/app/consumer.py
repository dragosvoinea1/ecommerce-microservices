# search-service/app/consumer.py
import pika
import json
import os
import time
from .es_client import get_es_client

def main():
    print(" [CONSUMER] Starting...")
    es = get_es_client() # Obține conexiunea
    if not es: return

    # Creează indexul dacă nu există
    if not es.indices.exists(index="products"):
        es.indices.create(index="products")
        print(" [CONSUMER] Created 'products' index.")

    # Conectare la RabbitMQ
    connection = pika.BlockingConnection(pika.URLParameters(os.environ.get("RABBITMQ_URL")))
    channel = connection.channel()
    channel.queue_declare(queue='product_events_queue', durable=True)
    print(' [CONSUMER] Waiting for messages.')

    def callback(ch, method, properties, body):
        print(f" [CONSUMER] Received message: {body.decode()}")
        data = json.loads(body)
        action, product = data.get('action'), data.get('product')
        product_id = product.get('id')
        try:
            if action in ['create', 'update']:
                es.index(index='products', id=product_id, document=product)
                print(f" [CONSUMER] Product {product_id} indexed.")
            elif action == 'delete':
                es.delete(index='products', id=product_id)
                print(f" [CONSUMER] Product {product_id} deleted.")
        except Exception as e:
            print(f" [!] Error processing message: {e}")

    channel.basic_consume(queue='product_events_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()