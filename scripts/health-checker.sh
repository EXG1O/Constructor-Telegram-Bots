#!/bin/bash

echo "Checking services health..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
  echo "Attempt $attempt/$max_attempts"

  postgres_ok=$(docker compose exec -T postgres pg_isready -U postgres 2>/dev/null | grep accepting)
  redis_ok=$(docker compose exec -T redis redis-cli ping 2>/dev/null | grep PONG)
  app_ok=$(curl -s http://localhost:8000 > /dev/null 2>&1 && echo "ok")

  if [ -n "$postgres_ok" ] && [ -n "$redis_ok" ] && [ -n "$app_ok" ]; then
    echo "Services healthy."
    break
  fi

  if [ $attempt -eq $max_attempts ]; then
    echo "Services health check failed."
    docker compose logs
    exit 1
  fi

  attempt=$((attempt + 1))
  sleep 3
done
