FROM python:3.9.13-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

RUN mkdir /tms
WORKDIR /tms

COPY ./requirements/dev-requirements.txt /tms/requirements/

RUN pip install -r requirements/dev-requirements.txt

COPY ./scripts/entrypoint.sh /tms/scripts/entrypoint.sh
RUN chmod +x /tms/scripts/entrypoint.sh

COPY . /tms

CMD ["/tms/scripts/entrypoint.sh"]