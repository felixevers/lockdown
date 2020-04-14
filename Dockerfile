FROM python:3.8-alpine

EXPOSE 80

WORKDIR /app

ADD . /app

RUN apk add gcc musl-dev libffi-dev libressl-dev

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn","--workers", "8", "app:create_app()", "--bind", "0.0.0.0:80"]