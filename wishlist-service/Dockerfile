# Folosește o imagine oficială Python ca bază
FROM python:3.10-slim

# Instalează supervisor
RUN apt-get update && apt-get install -y supervisor

# Setează directorul de lucru în container
WORKDIR /code

# Copiază fișierul de dependențe și instalează-le
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiază codul aplicației, testele și configurarea pytest
COPY ./app /code/app
COPY ./tests /code/tests
COPY ./pytest.ini /code/pytest.ini

# Copiază fișierul de configurare pentru supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY ./cleanup.py /code/cleanup.py

# Expune portul
EXPOSE 8000

# Pornește supervisor, care la rândul lui va porni uvicorn și consumer-ul
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]