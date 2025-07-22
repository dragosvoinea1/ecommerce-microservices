# Foloseste o imagine oficiala Python
FROM python:3.10-slim

# Seteaza directorul de lucru in container
WORKDIR /code

# Copiaza fisierul de dependinte si instaleaza-le
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiaza codul aplicatiei in container
COPY ./app /code/app

# Expune portul pe care va rula aplicatia
EXPOSE 8000

# Comanda pentru a porni serverul Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]