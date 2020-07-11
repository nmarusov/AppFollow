#! /usr/bin/env sh

# Exit in case of error
set -e

docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-compose.test.yml up -d
docker-compose -f docker-compose.test.yml exec -T backend bash /app/tests-start.sh "$@"
docker-compose -f docker-compose.test.yml down -v --remove-orphans
