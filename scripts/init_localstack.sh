#!/bin/sh

# Esperar a que LocalStack esté listo
until aws --endpoint-url=http://localhost:4566 sqs list-queues > /dev/null 2>&1; do
  echo "Esperando a que LocalStack esté disponible..."
  sleep 2
done

echo "LocalStack está listo."
