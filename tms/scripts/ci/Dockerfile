FROM python:3.9.13-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /tms
WORKDIR /tms

COPY ./tms/requirements/ci-requirements.txt /tms/requirements/
RUN pip install -r requirements/ci-requirements.txt

COPY . /tms