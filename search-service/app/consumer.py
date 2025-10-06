# search-service/app/consumer.py
import pika
import json
import os
import time
from .es_client import get_es_client

def main():
    print(" [SEARCH CONSUMER] Starting...")
    es = get_es_client()
    if not es: return

    if not es.indices.exists(index="products"):
        es.indices.create(index="products")
        print(" [SEARCH CONSUMER] Created 'products' index.")

    connection = pika.BlockingConnection(pika.URLParameters(os.environ.get("RABBITMQ_URL")))
    channel = connection.channel()

    channel.exchange_declare(exchange='product_events_exchange', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='product_events_exchange', queue=queue_name)
    print(f' [SEARCH CONSUMER] Waiting for messages on queue "{queue_name}".')

    def callback(ch, method, properties, body):
        print(f" [SEARCH CONSUMER] Received message: {body.decode()}")
        data = json.loads(body)
        action, product = data.get('action'), data.get('product')
        product_id = product.get('id')
        try:
            if action in ['create', 'update']:
                es.index(index='products', id=product_id, document=product)
                print(f" [SEARCH CONSUMER] Product {product_id} indexed.")
            elif action == 'delete':
                es.delete(index='products', id=product_id)
                print(f" [SEARCH CONSUMER] Product {product_id} deleted.")
            
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f" [!] Error processing message: {e}")

    # 4. Consumă din coada nou creată, nu din cea veche
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    
    channel.start_consuming()

if __name__ == '__main__':
    main()