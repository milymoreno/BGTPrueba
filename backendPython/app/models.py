import boto3
import os
from uuid import uuid4
from datetime import datetime


# Configura las variables de entorno para LocalStack
os.environ['AWS_ACCESS_KEY_ID'] = 'prueba'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'prueba'
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

# Inicializa el cliente de boto3 para DynamoDB apuntando a LocalStack
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566'  # URL de LocalStack
)

# Definir el nombre de la tabla
TABLE_NAME_CLIENTES = 'Clientes'
TABLE_NAME_FONDOS = 'Fondos'

# models.py

import boto3
from botocore.exceptions import ClientError

# Constantes para el nombre de las tablas y otras configuraciones
TABLE_NAME_CLIENTES = 'Clientes'
TABLE_NAME_FONDOS = 'Fondos'

# Función para crear las tablas (si no existen)import boto3
from botocore.exceptions import ClientError

TABLE_NAME_CLIENTES = 'Clientes'
TABLE_NAME_FONDOS = 'Fondos'

def create_tables():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')  # Configura el cliente de DynamoDB
    try:
        # Verificar si la tabla de Clientes ya existe
        existing_tables = dynamodb.meta.client.list_tables()['TableNames']
        if TABLE_NAME_CLIENTES not in existing_tables:
            table_clientes = dynamodb.create_table(
                TableName=TABLE_NAME_CLIENTES,
                KeySchema=[
                    {'AttributeName': 'Id', 'KeyType': 'HASH'}  # Clave primaria
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'Id', 'AttributeType': 'S'},  # Tipo de atributo String
                    {'AttributeName': 'numeroIdentificacion', 'AttributeType': 'S'}  # Atributo para el índice global
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'NumeroIdentificacionIndex',
                        'KeySchema': [
                            {'AttributeName': 'numeroIdentificacion', 'KeyType': 'HASH'}
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ]
            )
            table_clientes.wait_until_exists()
            print(f"Tabla {TABLE_NAME_CLIENTES} creada exitosamente.")
        else:
            print(f"La tabla {TABLE_NAME_CLIENTES} ya existe. No es necesario crearla.")

        # Verificar si la tabla de Fondos ya existe
        if TABLE_NAME_FONDOS not in existing_tables:
            table_fondos = dynamodb.create_table(
                TableName=TABLE_NAME_FONDOS,
                KeySchema=[
                    {'AttributeName': 'fondoId', 'KeyType': 'HASH'}  # Clave primaria
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'fondoId', 'AttributeType': 'S'}  # Tipo de atributo String
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            table_fondos.wait_until_exists()
            print(f"Tabla {TABLE_NAME_FONDOS} creada exitosamente.")
        else:
            print(f"La tabla {TABLE_NAME_FONDOS} ya existe. No es necesario crearla.")

    except ClientError as e:
        print(f"Error al crear o verificar las tablas: {e.response['Error']['Message']}")


# Funciones para operar sobre la tabla

# Clientes
def add_cliente(cliente):
    table = dynamodb.Table(TABLE_NAME_CLIENTES)
    table.put_item(Item=cliente)

def get_cliente(cliente_id):
    table = dynamodb.Table(TABLE_NAME_CLIENTES)
    response = table.get_item(Key={'Id': cliente_id})
    return response.get('Item')

def update_cliente(cliente_id, update_expression, expression_attribute_values):
    table = dynamodb.Table(TABLE_NAME_CLIENTES)
    response = table.update_item(
        Key={'Id': cliente_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="UPDATED_NEW"
    )
    return response

def delete_cliente(cliente_id):
    table = dynamodb.Table(TABLE_NAME_CLIENTES)
    response = table.delete_item(Key={'Id': cliente_id})
    return response

def add_transaccion(cliente_id, transaccion):
    # Obtener la tabla DynamoDB
    table_clientes = dynamodb.Table(TABLE_NAME_CLIENTES)
    
    try:
        # Agregar la transacción al historial de transacciones del cliente
        response = table_clientes.update_item(
            Key={'Id': cliente_id},
            UpdateExpression="SET historialTransacciones = list_append(if_not_exists(historialTransacciones, :empty_list), :new_transaccion)",
            ExpressionAttributeValues={
                ':new_transaccion': [transaccion],
                ':empty_list': []
            },
            ReturnValues="ALL_NEW"
        )
        cliente_actualizado = response.get('Attributes')
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
    
    # Funciones para operar sobre la tabla Fondos
def add_fondo(fondo):
    table = dynamodb.Table(TABLE_NAME_FONDOS)
    table.put_item(Item=fondo)

def get_fondos():
    table = dynamodb.Table(TABLE_NAME_FONDOS)
    response = table.scan()
    return response.get('Items')

def get_fondo(fondo_id):
    table = dynamodb.Table(TABLE_NAME_FONDOS)
    response = table.get_item(Key={'fondoId': fondo_id})
    return response.get('Item')



# Estructuras de ejemplo
cliente_example = {
    "Id": str(uuid4()), 
    "Nombres": "Nombres del Cliente",
    "Apellidos": "Apellidos del Cliente",
    "tipoIdentificacion": "Tipo identificacion del Cliente",
    "numeroIdentificacion": "Numero de identificacion del Cliente",
    "Email": "cliente@example.com",
    "Telefono": "123456789",
    "saldoActual": 500000,
    "preferenciaNotificacion": "email",
    "fondosSuscritos": [
        {
            "fondoId": str(uuid4()),
            "montoSuscrito": 500000,
            "fechaSuscripcion": datetime.utcnow().isoformat()
        }
    ],
    "historialTransacciones": [
        {
            "transactionId": str(uuid4()),
            "fondoId": str(uuid4()),
            "tipo": "apertura",
            "monto": 500000,
            "fecha": datetime.utcnow().isoformat()
        }
    ]
}


