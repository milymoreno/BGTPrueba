#!/bin/sh

# Crear tabla Clientes en DynamoDB con _id como UUID generado automáticamente
aws dynamodb create-table \
    --table-name Clientes \
    --attribute-definitions \
		AttributeName=Id,AttributeType=S \
    --key-schema AttributeName=Id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --endpoint-url http://localhost:4566 \
	
sleep 2
	
aws dynamodb create-table \
    --table-name Fondos \
    --attribute-definitions \
        AttributeName=fondoId,AttributeType=S \
    --key-schema AttributeName=fondoId,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --endpoint-url http://localhost:4566 \
	
sleep 2
	
	
aws dynamodb create-table \
    --table-name HistorialTransacciones \
    --attribute-definitions \
        AttributeName=TransaccionId,AttributeType=S \
		AttributeName=clienteId,AttributeType=S \
    --key-schema AttributeName=TransaccionId,KeyType=HASH AttributeName=clienteId,KeyType=RANGE  \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --endpoint-url http://localhost:4566 \

sleep 2
	
