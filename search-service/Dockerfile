FROM python:3.10-slim

# Instalează supervisor
RUN apt-get update && apt-get install -y supervisor

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./tests /code/tests
COPY ./pytest.ini /code/pytest.ini
# Copiază fișierul de configurare pentru supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

# Pornește supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]