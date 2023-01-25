FROM registry.spb.yadro.com/tools/python:3.9.13-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd && apk add build-base openldap-dev python3-dev

RUN mkdir /testy
WORKDIR /testy

COPY ./requirements/requirements.txt /testy/requirements/

RUN pip install -r requirements/requirements.txt

COPY ./scripts/entrypoint.sh /testy/scripts/entrypoint.sh
RUN chmod +x /testy/scripts/entrypoint.sh

COPY . /testy

WORKDIR /testy/testy
CMD ["/testy/testy/scripts/entrypoint.sh"]
