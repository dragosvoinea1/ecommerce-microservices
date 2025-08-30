import pika
import json
import os
import time
from elasticsearch import Elasticsearch

# Așteptăm puțin pentru ca Elasticsearch să pornească complet
time.sleep(15)

print(' [*] Search consumer script started.')

# Conexiunea la Elasticsearch
ES_HOST = os.environ.get("ELASTICSEARCH_HOST")
es = Elasticsearch([{'host': ES_HOST, 'port': 9200, 'scheme': 'http'}])

# Conexiunea la RabbitMQ
RABBITMQ_URL = os.environ.get("RABBITMQ_URL")
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
channel = connection.channel()

# Declarăm exchange-ul (vom folosi un fanout pentru a trimite mesajul la mai mulți consumatori în viitor)
channel.exchange_declare(exchange='products_exchange', exchange_type='fanout')

# Creăm o coadă temporară, care va fi ștearsă la ieșire
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Legăm coada de exchange
channel.queue_bind(exchange='products_exchange', queue=queue_name)

def callback(ch, method, properties, body):
    """Procesează mesajele primite."""
    print(f" [x] Received message: {body.decode()}")
    data = json.loads(body)
    action = data.get('action')
    product = data.get('product')

    try:
        if action == 'create' or action == 'update':
            es.index(index='products', id=product['id'], document=product)
            print(f" [x] Product {product['id']} indexed/updated in Elasticsearch.")
        elif action == 'delete':
            es.delete(index='products', id=product['id'])
            print(f" [x] Product {product['id']} deleted from Elasticsearch.")
    except Exception as e:
        print(f" [!] Error processing message: {e}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()