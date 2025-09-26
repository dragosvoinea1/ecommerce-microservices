# Folosește o imagine oficială Python ca bază
FROM python:3.10-slim

# Setează directorul de lucru în container
WORKDIR /code

# Copiază fișierul de dependențe și instalează-le
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiază codul aplicației, testele și configurarea pytest
COPY ./app /code/app
COPY ./tests /code/tests
COPY ./pytest.ini /code/pytest.ini

# Expune portul pe care va rula aplicația
EXPOSE 8000

# Comanda pentru a porni serverul Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]