import os
import httpx
import json
import pika
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from . import models, db

# --- Configurare ---
models.Base.metadata.create_all(bind=db.engine)

ROOT_PATH = os.environ.get("ROOT_PATH", "")
app = FastAPI(title="Orders Service", root_path=ROOT_PATH)

# Adresele celorlalte servicii, citite din variabilele de mediu
PRODUCTS_SERVICE_URL = os.environ.get("PRODUCTS_SERVICE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

# --- MODIFICARE: Folosim o schema mai simpla pentru a accepta token-ul ---
api_key_header_scheme = APIKeyHeader(name="Authorization")


# --- Dependințe ---
def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()


async def get_current_user_email(token: str = Security(api_key_header_scheme)):
    """
    Extrage token-ul din header, validează-l și returnează email-ul.
    Header-ul trebuie să fie: 'Authorization: Bearer <token>'
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    # Verificăm dacă token-ul începe cu "Bearer "
    if not token.startswith("Bearer "):
        raise credentials_exception

    # Eliminăm "Bearer " pentru a obține token-ul pur
    token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception


RABBITMQ_URL = os.environ.get("RABBITMQ_URL")


# --- Endpoints API ---
@app.post("/orders",
          response_model=models.Order,
          status_code=status.HTTP_201_CREATED)
async def create_order(order_data: models.OrderCreate,
                       db: Session = Depends(get_db),
                       owner_email: str = Depends(get_current_user_email)):
    """
    Creează o comandă nouă.
    """
    total_amount = 0
    order_items_to_create = []
    products_to_update_stock = []

    async with httpx.AsyncClient() as client:
        for item in order_data.items:
            try:
                response = await client.get(
                    f"{PRODUCTS_SERVICE_URL}/products/{item.product_id}")
                response.raise_for_status()
                product = response.json()

                if product['stock'] < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Stoc insuficient pentru produsul ID {item.product_id}. Stoc disponibil: {product['stock']}"
                    )

                price_at_purchase = product['price']
                total_amount += price_at_purchase * item.quantity
                order_items_to_create.append({
                    "product_id":
                    item.product_id,
                    "quantity":
                    item.quantity,
                    "price_at_purchase":
                    price_at_purchase
                })
                products_to_update_stock.append({  # <-- Adăugăm aici
                    "product_id": item.product_id,
                    "quantity": item.quantity
                })

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Produsul cu ID {item.product_id} nu a fost găsit.")
                else:
                    raise HTTPException(
                        status_code=503,
                        detail="Serviciul de produse nu este disponibil.")

    new_order = models.DBOrder(owner_email=owner_email,
                               total_amount=total_amount)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item_data in order_items_to_create:
        db_item = models.DBOrderItem(**item_data, order_id=new_order.id)
        db.add(db_item)

    db.commit()
    db.refresh(new_order)

    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue='stock_update_queue')

        message_body = json.dumps({
            "order_id": new_order.id,
            "products": products_to_update_stock
        })

        channel.basic_publish(exchange='',
                              routing_key='stock_update_queue',
                              body=message_body)
        connection.close()
        print(f" [x] Sent stock update message for order {new_order.id}")
    except Exception as e:
        # Într-o aplicație reală, am loga eroarea și am avea un mecanism de reîncercare
        print(f"Error publishing to RabbitMQ: {e}")

    return new_order


@app.get("/orders", response_model=List[models.Order])
async def get_user_orders(db: Session = Depends(get_db),
                          owner_email: str = Depends(get_current_user_email)):
    """Returnează istoricul de comenzi pentru utilizatorul autentificat."""
    orders = db.query(models.DBOrder).filter(
        models.DBOrder.owner_email == owner_email).all()
    return orders
