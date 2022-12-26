FROM python:3.9.13-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd && apk add build-base openldap-dev python3-dev

RUN mkdir /testy
WORKDIR /testy

COPY ./requirements/dev-requirements.txt /testy/requirements/

RUN pip install -r requirements/dev-requirements.txt

COPY ./migrator/ /testy/migrator
RUN pip install -e migrator