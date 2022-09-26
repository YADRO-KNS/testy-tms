FROM python:3.9.13-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

RUN mkdir /tms
WORKDIR /tms

COPY ./dev-requirements.txt /tms/dev-requirements.txt

RUN pip install -r dev-requirements.txt

COPY ./scripts/entrypoint.sh /tms/entrypoint.sh
RUN chmod +x /tms/entrypoint.sh

COPY . /tms

CMD ["/tms/entrypoint.sh"]