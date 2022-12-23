FROM python:3.9.13-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

RUN mkdir /testy
WORKDIR /testy

COPY ./requirements/dev-requirements.txt /testy/requirements/
COPY ./migrator /testy/migrator

RUN pip install -r requirements/dev-requirements.txt
RUN pip install -e /testy/migrator

COPY ./scripts/entrypoint.sh /testy/scripts/entrypoint.sh
RUN chmod +x /testy/scripts/entrypoint.sh

COPY . /testy

WORKDIR /testy/testy
CMD ["/testy/testy/scripts/entrypoint.sh"]