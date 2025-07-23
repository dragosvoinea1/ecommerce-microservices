FROM python:3.10-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

# --- NOU: Copiem și facem executabil scriptul de pornire ---
COPY ./start.sh /code/start.sh
RUN chmod +x /code/start.sh

EXPOSE 8000
# --- MODIFICAT: Rulăm scriptul de pornire în loc de uvicorn direct ---
CMD ["/code/start.sh"]