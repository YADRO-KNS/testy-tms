#!/bin/bash


fails=""

inspect() {
  # Usage: inspect $? lint
  # * param1: job result code
  # * param2: job name
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

lint() {
  docker-compose -f docker-compose-ci.yml up -d --build
  docker-compose -f docker-compose-ci.yml run --rm  testy-ci flake8 .
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