FROM python:3.10-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
EXPOSE 8000

CMD ["sh", "-c", "python /code/app/consumer.py & exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]