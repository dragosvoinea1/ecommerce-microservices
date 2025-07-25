import os
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite toate originile (pentru dezvoltare)
    allow_credentials=True,
    allow_methods=["*"],  # Permite toate metodele (GET, POST, etc.)
    allow_headers=["*"],  # Permite toate headerele
)

PRODUCTS_SERVICE_URL = os.environ.get("PRODUCTS_SERVICE_URL")
USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL")
ORDERS_SERVICE_URL = os.environ.get("ORDERS_SERVICE_URL")

client = httpx.AsyncClient()

@app.get("/")
def read_root():
    return {"message": "API Gateway is running"}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def reverse_proxy(request: Request, path: str):
    target_service_url = None
    
    # Logica de rutare simplificată
    first_segment = path.split('/')[0]

    if first_segment == "products":
        target_service_url = PRODUCTS_SERVICE_URL
    elif first_segment in ["users", "login", "register"]:
        target_service_url = USER_SERVICE_URL
    elif first_segment == "orders":
        target_service_url = ORDERS_SERVICE_URL
    
    if not target_service_url:
        return Response(status_code=404, content="Not Found")

    target_url = f"{target_service_url}/{path}"
    headers = dict(request.headers)
    headers["host"] = httpx.URL(target_url).host
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
        return Response(content=r.content, status_code=r.status_code, headers=dict(r.headers))
    except httpx.RequestError as e:
        return Response(status_code=503, content=f"Service unavailable: {e}")