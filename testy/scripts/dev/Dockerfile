###########
# BUILDER #
###########

FROM node:12.22.12-alpine AS builder

RUN mkdir /frontend
WORKDIR /frontend

ENV PATH /frontend/node_modules/.bin:$PATH
COPY  ./testy_static/apps/test-runs-app /frontend/test-runs-app
COPY  ./testy_static/apps/test-suites-app /frontend/test-suites-app

# set environment variables
ARG REACT_APP_API_ROOT
ENV REACT_APP_API_ROOT $REACT_APP_API_ROOT
ARG NODE_ENV
ENV NODE_ENV $NODE_ENV

RUN cd /frontend/test-runs-app && npm install && npm run build
RUN cd /frontend/test-suites-app && npm install && npm run build

############
# FINISHED #
############

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

RUN pip install -r requirements/dev-requirements.txt

COPY ./scripts/entrypoint.sh /testy/scripts/entrypoint.sh
RUN chmod +x /testy/scripts/entrypoint.sh

COPY . /testy

# copy static files
RUN mkdir -p /testy/testy_static/dist/assets/js/apps
COPY --from=builder /frontend/test-runs-app/build/test-runs-app.js /testy/testy_static/dist/assets/js/apps
COPY --from=builder /frontend/test-suites-app/build/test-suites-app.js /testy/testy_static/dist/assets/js/apps

CMD ["/testy/scripts/entrypoint.sh"]