# Folosește o imagine oficială Python ca bază
FROM python:3.10-slim

# Setează directorul de lucru în container
WORKDIR /code

# Copiază fișierul de dependențe și instalează-le
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiază codul aplicației în container
COPY ./app /code/app

# Expune portul pe care va rula aplicația
EXPOSE 8000

# Comanda pentru a porni serverul Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]