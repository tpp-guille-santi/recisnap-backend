#!/bin/sh
#
docker compose -f docker-compose.test.yml build
docker compose -f docker-compose.test.yml run --entrypoint "pytest --cov --cov-report term-missing:skip-covered" web
docker compose -f docker-compose.test.yml down --remove-orphans
