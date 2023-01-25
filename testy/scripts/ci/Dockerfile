FROM python:3.9.13-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /testy
WORKDIR /testy

COPY ./testy/requirements/ci-requirements.txt /testy/requirements/

RUN apk add build-base openldap-dev python3-dev

RUN pip install -r requirements/ci-requirements.txt

COPY . /testy