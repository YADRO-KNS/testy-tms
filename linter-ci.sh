#!/bin/bash


fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

lint() {
  docker-compose -f docker-compose-ci.yml up -d --build
  docker-compose -f docker-compose-ci.yml run --rm  tms-ci flake8 .
  inspect $? lint
  docker-compose -f docker-compose-ci.yml down -v
}

echo "Running linter!"
lint

if [ -n "${fails}" ]; then
  echo "Linter failed: ${fails}"
  exit 1
else
  echo "Linter passed!"
  exit 0
fi