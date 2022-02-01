FROM python:3.9.10-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN groupadd app && useradd app && usermod -a -G app app


RUN mkdir /app && chown app:app /app


USER app

WORKDIR /app


RUN pip install pipenv

COPY . .

RUN pipenv install --system --deploy

RUN  chmod +x  ./entrypoint.sh
RUN  chmod +x  ./entrypoint.sh


EXPOSE 8000