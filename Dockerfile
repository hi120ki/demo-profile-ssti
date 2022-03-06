FROM python:alpine

ENV CLOUD_SECRET_KEY 8Z0MH8EWYMB0N439

WORKDIR /app

RUN pip install -U flask

COPY ./ /app

CMD ["python", "main.py"]
