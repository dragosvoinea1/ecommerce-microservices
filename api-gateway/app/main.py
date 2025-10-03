import os
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import websockets 
import asyncio 
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect 

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCTS_SERVICE_URL = os.environ.get("PRODUCTS_SERVICE_URL")
USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL")
ORDERS_SERVICE_URL = os.environ.get("ORDERS_SERVICE_URL")
SEARCH_SERVICE_URL = os.environ.get("SEARCH_SERVICE_URL")
REVIEWS_SERVICE_URL = os.environ.get("REVIEWS_SERVICE_URL")
WISHLIST_SERVICE_URL = os.environ.get("WISHLIST_SERVICE_URL")
NOTIFICATIONS_SERVICE_URL = os.environ.get("NOTIFICATIONS_SERVICE_URL")

client = httpx.AsyncClient()

@app.get("/")
def read_root():
    return {"message": "API Gateway is running"}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def reverse_proxy(request: Request, path: str):
    target_service_url = None

    first_segment = path.split('/')[0]

    if first_segment == "products":
        target_service_url = PRODUCTS_SERVICE_URL
    elif first_segment in [
            "users", "login", "register", "confirm", "forgot-password",
            "reset-password"
    ]:
        target_service_url = USER_SERVICE_URL
    elif first_segment == "orders":
        target_service_url = ORDERS_SERVICE_URL
    elif first_segment == "search":
        target_service_url = SEARCH_SERVICE_URL
    elif first_segment == "reviews":
        target_service_url = REVIEWS_SERVICE_URL
    elif first_segment == "wishlist": # <-- ADAUGĂ ASTA
        target_service_url = WISHLIST_SERVICE_URL
    elif first_segment == "notifications": # <-- ADAUGĂ ASTA
        target_service_url = NOTIFICATIONS_SERVICE_URL
    if not target_service_url:
        return Response(status_code=404, content="Not Found")

    # Am eliminat logica `if request.query_params` de aici
    target_url = f"{target_service_url}/{path}"

    headers = dict(request.headers)
    headers["host"] = httpx.URL(target_service_url).host
    body = await request.body()

    try:
        r = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.query_params,
            content=body,
            timeout=10.0,
        )
        return Response(content=r.content,
                        status_code=r.status_code,
                        headers=dict(r.headers))
    except httpx.RequestError as e:
        return Response(status_code=503, content=f"Service unavailable: {e}")


@app.websocket("/ws/{path:path}")
async def websocket_proxy(websocket: WebSocket, path: str):
    await websocket.accept()
    target_url = f"ws://notifications-service:8000/ws/{path}"
    
    try:
        async with websockets.connect(target_url) as upstream_ws:
            
            # Funcție care citește de la client și scrie către serviciul de notificări
            async def forward_client_to_upstream():
                try:
                    while True:
                        data = await websocket.receive_text()
                        await upstream_ws.send(data)
                except WebSocketDisconnect:
                    pass # Ieșim elegant când clientul se deconectează

            # Funcție care citește de la serviciul de notificări și scrie către client
            async def forward_upstream_to_client():
                try:
                    while True:
                        data = await upstream_ws.recv() # Metoda corectă este .recv()
                        await websocket.send_text(data)
                except websockets.exceptions.ConnectionClosed:
                    pass # Ieșim elegant când serviciul închide conexiunea

            # Rulăm ambele funcții în paralel
            done, pending = await asyncio.wait(
                [forward_client_to_upstream(), forward_upstream_to_client()],
                return_when=asyncio.FIRST_COMPLETED,
            )
            
            # Anulăm task-ul care a rămas în așteptare pentru a elibera resursele
            for task in pending:
                task.cancel()

    except Exception as e:
        print(f"Eroare în proxy-ul WebSocket: {e}")
    finally:
        print("Proxy WebSocket: închidere conexiune.")