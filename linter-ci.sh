#!/bin/bash

exit_status=0

echo "Running linter!"
docker-compose -f docker-compose-ci.yml up -d --build
docker-compose -f docker-compose-ci.yml run --rm tms-ci flake8 .
exit_status=$?
docker-compose -f docker-compose-ci.yml down -v

exit $exit_status