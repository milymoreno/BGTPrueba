import boto3
import os
from datetime import datetime
from uuid import uuid4
#from flask import jsonify
from models import add_cliente, get_cliente, update_cliente, get_fondo
from decimal import Decimal  # Importa Decimal desde el módulo decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from uuid import uuid4


# Inicializa el cliente de boto3 para DynamoDB apuntando a LocalStack
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566'  # URL de LocalStack
)

# Definir el nombre de la tabla
TABLE_NAME_CLIENTES = 'Clientes'
TABLE_NAME_FONDOS = 'Fondos'

# Definir los nombres de las tablas
TABLE_NAME_CLIENTES = 'Clientes'
TABLE_NAME_FONDOS = 'Fondos'

"""
def add_fondo_suscrito(cliente_id, fondos):
    cliente = get_cliente(cliente_id)
    if not cliente:
        return None, 'Cliente no encontrado', 404

    if "fondosSuscritos" not in cliente:
        cliente["fondosSuscritos"] = []

    if "historialTransacciones" not in cliente:
        cliente["historialTransacciones"] = []

    for fondo in fondos:
        fondo_id = fondo.get('fondoId')
        monto_suscrito = fondo.get('montoSuscrito')

        # Obtener el fondo desde DynamoDB
        fondo_data = get_fondo(fondo_id)
        if not fondo_data:
            return None, f'Fondo {fondo_id} no encontrado', 404

       # Manejar monto mínimo (si existe)
        if 'montoMinimo' in fondo_data:
            monto_minimo = Decimal(fondo_data['montoMinimo'])
        else:
            monto_minimo = Decimal('0')  # Establecer un valor por defecto si no hay monto mínimo

        # Verificar si el saldo del cliente es suficiente
        saldo_actual = Decimal(cliente.get('saldoActual', 0))
        if saldo_actual < monto_minimo:
            return None, f'No tiene saldo disponible para vincularse al fondo {fondo_data.get("nombre", "desconocido")}', 400

        # Restar el monto suscrito del saldo actual del cliente
        nuevo_saldo = saldo_actual - Decimal(monto_suscrito)
        if nuevo_saldo < 0:
            return None, f'No tiene saldo suficiente para suscribirse a {fondo_data.get("nombre", "desconocido")}', 400

        cliente['saldoActual'] = nuevo_saldo

        # Agregar el fondo suscrito al cliente
        if "fechaSuscripcion" not in fondo:
            fondo["fechaSuscripcion"] = datetime.utcnow().isoformat()

        cliente["fondosSuscritos"].append(fondo)

        # Crear una transacción de apertura para el fondo suscrito
        transaccion_apertura = {
            "transactionId": str(uuid4()),
            "fondoId": fondo["fondoId"],
            "tipo": "apertura",
            "monto": fondo["montoSuscrito"],
            "fecha": fondo["fechaSuscripcion"]
        }
        cliente["historialTransacciones"].append(transaccion_apertura)

    update_expression = "SET fondosSuscritos = :fondosSuscritos, historialTransacciones = :historialTransacciones, saldoActual = :saldoActual"
    expression_attribute_values = {
        ':fondosSuscritos': cliente["fondosSuscritos"],
        ':historialTransacciones': cliente["historialTransacciones"],
        ':saldoActual': cliente["saldoActual"]
    }
    try:
        update_cliente(cliente_id, update_expression, expression_attribute_values)
    except Exception as e:
        print(f'Error al actualizar el cliente: {str(e)}')
        return f'Error al actualizar el cliente: {str(e)}', 500

    # Retornar el cliente actualizado y un mensaje de éxito
    return get_cliente(cliente_id), 'Fondos suscritos correctamente', 200
"""

def add_fondo_suscrito(cliente_id, fondos):
    print(f'Entre a funcion')
    cliente = get_cliente(cliente_id)
    if not cliente:
        print(f'Cliente no encontrado para ID: {cliente_id}')
        return None, 'Cliente no encontrado', 404

    print(f'Cliente encontrado: {cliente}')

    if "fondosSuscritos" not in cliente:
        cliente["fondosSuscritos"] = []

    if "historialTransacciones" not in cliente:
        cliente["historialTransacciones"] = []

    for fondo in fondos:
        fondo_id = fondo.get('fondoId')
        monto_suscrito = fondo.get('montoSuscrito')

        print(f'Procesando fondo {fondo_id} con monto suscrito {monto_suscrito}')

        # Obtener el fondo desde DynamoDB
        fondo_data = get_fondo(fondo_id)
        if not fondo_data:
            print(f'Fondo {fondo_id} no encontrado en la base de datos')
            return None, f'Fondo {fondo_id} no encontrado', 404

        print(f'Fondo {fondo_id} encontrado: {fondo_data}')

        # Manejar monto mínimo (si existe)
        monto_minimo = Decimal(fondo_data.get('montoMinimo', '0'))

        # Verificar si el saldo del cliente es suficiente
        saldo_actual = Decimal(cliente.get('saldoActual', 0))
        if saldo_actual < monto_minimo:
            print(f'Saldo insuficiente para suscribirse al fondo {fondo_id}')
            return None, f'No tiene saldo suficiente para suscribirse a {fondo_data.get("nombre", "desconocido")}', 400

        # Restar el monto suscrito del saldo actual del cliente
        nuevo_saldo = saldo_actual - Decimal(monto_suscrito)
        if nuevo_saldo < 0:
            print(f'Saldo insuficiente para suscribirse al fondo {fondo_id}')
            return None, f'No tiene saldo suficiente para suscribirse a {fondo_data.get("nombre", "desconocido")}', 400

        print(f'Saldo suficiente para suscribirse al fondo {fondo_id}')

        cliente['saldoActual'] = nuevo_saldo

        # Agregar el fondo suscrito al cliente
        if "fechaSuscripcion" not in fondo:
            fondo["fechaSuscripcion"] = datetime.utcnow().isoformat()

        cliente["fondosSuscritos"].append(fondo)

        print(f'Fondo {fondo_id} suscrito correctamente')

        # Crear una transacción de apertura para el fondo suscrito
        transaccion_apertura = {
            "transactionId": str(uuid4()),
            "fondoId": fondo["fondoId"],
            "tipo": "apertura",
            "monto": fondo["montoSuscrito"],
            "fecha": fondo["fechaSuscripcion"]
        }
        cliente["historialTransacciones"].append(transaccion_apertura)

        print(f'Transacción de apertura creada para fondo {fondo_id}')

    # Actualizar el cliente en DynamoDB después de suscribir todos los fondos
    update_expression = "SET fondosSuscritos = :fondosSuscritos, historialTransacciones = :historialTransacciones, saldoActual = :saldoActual"
    expression_attribute_values = {
        ':fondosSuscritos': cliente["fondosSuscritos"],
        ':historialTransacciones': cliente["historialTransacciones"],
        ':saldoActual': cliente["saldoActual"]
    }

    try:
        update_cliente(cliente_id, update_expression, expression_attribute_values)
        print(f'Cliente actualizado en la base de datos: {cliente}')
    except Exception as e:
        print(f'Error al actualizar el cliente: {str(e)}')
        return None, f'Error al actualizar el cliente: {str(e)}', 500

    # Retornar el cliente actualizado y un mensaje de éxito
    return cliente, 'Fondos suscritos correctamente', 200



#Cancelaciones


def cancelar_suscripcion(cliente_id, fondos_a_cancelar):
    fecha_cancelacion = datetime.utcnow().isoformat()

    # Obtener el cliente desde DynamoDB
    table_clientes = dynamodb.Table(TABLE_NAME_CLIENTES)
    response = table_clientes.get_item(Key={'Id': cliente_id})
    cliente = response.get('Item')

    # Verificar si el cliente existe
    if not cliente:
        print('Cliente no encontrado')
        return 'Cliente no encontrado', 404

    print(f"Cliente encontrado: {cliente}")

    for fondo_a_cancelar in fondos_a_cancelar:
        fondo_id = fondo_a_cancelar.get('fondoId')
        print(f"Intentando cancelar suscripción del fondo: {fondo_id}")

        # Buscar el fondo en los fondos suscritos del cliente
        fondo_encontrado = None
        for fondo in cliente.get('fondosSuscritos', []):
            print(f"Comparando con fondo suscrito: {fondo['fondoId']}")
            if fondo['fondoId'] == fondo_id:
                fondo_encontrado = fondo
                break

        # Verificar si el fondo fue encontrado en los fondos suscritos del cliente
        if not fondo_encontrado:
            print(f"El fondo {fondo_id} no está suscrito por el cliente")
            return f'El fondo {fondo_id} no está suscrito por el cliente', 404

        print(f"Fondo encontrado: {fondo_encontrado}")

        # Devolver el monto suscrito al saldo del cliente
        cliente['saldoActual'] += Decimal(fondo_encontrado['montoSuscrito'])

        # Eliminar el fondo de los fondos suscritos del cliente
        cliente['fondosSuscritos'].remove(fondo_encontrado)

        # Generar una transacción de cancelación
        transaction_id = str(uuid4())  # Generar un nuevo UUID para la transacción
        monto_cancelado = fondo_encontrado['montoSuscrito']
        
        # Crear una transacción de cancelación para el fondo suscrito
        transaccion_cancelacion = {
            'transactionId': transaction_id,
            'fondoId': fondo_encontrado['fondoId'],
            'tipo': 'cancelacion',
            'monto': monto_cancelado,
            'fecha': fecha_cancelacion
        }

        # Agregar la transacción de cancelación al historial de transacciones del cliente
        if 'historialTransacciones' not in cliente:
            cliente['historialTransacciones'] = []

        cliente['historialTransacciones'].append(transaccion_cancelacion)

    # Actualizar el cliente en DynamoDB después de cancelar todas las suscripciones
    update_expression = "SET fondosSuscritos = :fondosSuscritos, historialTransacciones = :historialTransacciones, saldoActual = :saldoActual"
    expression_attribute_values = {
        ':fondosSuscritos': cliente["fondosSuscritos"],
        ':historialTransacciones': cliente["historialTransacciones"],
        ':saldoActual': cliente["saldoActual"]
    }

    try:
        update_cliente(cliente_id, update_expression, expression_attribute_values)
    except Exception as e:
        print(f'Error al actualizar el cliente: {str(e)}')
        return f'Error al actualizar el cliente: {str(e)}', 500
   
    return get_cliente(cliente_id), 'Fondos cancelados correctamente', 200 

"""
def add_fondo_suscrito(cliente_id, fondos):
    cliente = get_cliente(cliente_id)
    
    if not cliente:
        return None, 'Cliente no encontrado', 404

    if "fondosSuscritos" not in cliente:
        cliente["fondosSuscritos"] = []

    for fondo in fondos:
        fondo_id = fondo.get('fondoId')
        monto_suscrito = fondo.get('montoSuscrito')

        # Obtener el fondo desde DynamoDB
        fondo_data = get_fondo(fondo_id)
        if not fondo_data:
            return None, f'Fondo {fondo_id} no encontrado', 404

        # Manejar monto mínimo (si existe)
        monto_minimo = Decimal(fondo_data.get('montoMinimo', '0'))

        # Verificar si el saldo del cliente es suficiente
        saldo_actual = Decimal(cliente.get('saldoActual', 0))
        if saldo_actual < monto_minimo:
            return None, f'No tiene saldo disponible para vincularse al fondo {fondo_data.get("nombre", "desconocido")}', 400

        # Restar el monto suscrito del saldo actual del cliente
        nuevo_saldo = saldo_actual - Decimal(monto_suscrito)
        if nuevo_saldo < 0:
            return None, f'No tiene saldo suficiente para suscribirse a {fondo_data.get("nombre", "desconocido")}', 400

        cliente['saldoActual'] = nuevo_saldo

        # Agregar el fondo suscrito al cliente
        if "fechaSuscripcion" not in fondo:
            fondo["fechaSuscripcion"] = datetime.utcnow().isoformat()

        cliente["fondosSuscritos"].append(fondo)

        # Crear una transacción de apertura para el fondo suscrito
        transaccion_apertura = {
            "transactionId": str(uuid4()),
            "fondoId": fondo["fondoId"],
            "tipo": "apertura",
            "monto": fondo["montoSuscrito"],
            "fecha": fondo["fechaSuscripcion"]
        }

        # Utilizar la función realizar_transaccion para registrar la transacción
        _, mensaje, status_code = realizar_transaccion(cliente_id, transaccion_apertura)

        if status_code != 200:
            return None, mensaje, status_code

    # Actualizar el cliente en DynamoDB después de suscribir todos los fondos
    update_expression = "SET fondosSuscritos = :fondosSuscritos, saldoActual = :saldoActual"
    expression_attribute_values = {
        ':fondosSuscritos': cliente["fondosSuscritos"],
        ':saldoActual': cliente["saldoActual"]
    }

    try:
        update_cliente(cliente_id, update_expression, expression_attribute_values)
    except Exception as e:
        print(f'Error al actualizar el cliente: {str(e)}')
        return None, f'Error al actualizar el cliente: {str(e)}', 500

    # Retornar el cliente actualizado y un mensaje de éxito
    return get_cliente(cliente_id), 'Fondos suscritos correctamente', 200


def cancelar_suscripcion(cliente_id, fondos_a_cancelar):
    fecha_cancelacion = datetime.utcnow().isoformat()

    # Obtener el cliente desde DynamoDB
    cliente = get_cliente(cliente_id)

    # Verificar si el cliente existe
    if not cliente:
        print('Cliente no encontrado')
        return 'Cliente no encontrado', 404

    print(f"Cliente encontrado: {cliente}")

    for fondo_a_cancelar in fondos_a_cancelar:
        fondo_id = fondo_a_cancelar.get('fondoId')
        print(f"Intentando cancelar suscripción del fondo: {fondo_id}")

        # Buscar el fondo en los fondos suscritos del cliente
        fondo_encontrado = None
        for fondo in cliente.get('fondosSuscritos', []):
            print(f"Comparando con fondo suscrito: {fondo['fondoId']}")
            if fondo['fondoId'] == fondo_id:
                fondo_encontrado = fondo
                break

        # Verificar si el fondo fue encontrado en los fondos suscritos del cliente
        if not fondo_encontrado:
            print(f"El fondo {fondo_id} no está suscrito por el cliente")
            return f'El fondo {fondo_id} no está suscrito por el cliente', 404

        print(f"Fondo encontrado: {fondo_encontrado}")

        # Devolver el monto suscrito al saldo del cliente
        cliente['saldoActual'] += Decimal(fondo_encontrado['montoSuscrito'])

        # Eliminar el fondo de los fondos suscritos del cliente
        cliente['fondosSuscritos'].remove(fondo_encontrado)

        # Crear una transacción de cancelación
        transaccion_cancelacion = {
            'transactionId': str(uuid4()),
            'fondoId': fondo_encontrado['fondoId'],
            'tipo': 'cancelacion',
            'monto': fondo_encontrado['montoSuscrito'],
            'fecha': fecha_cancelacion
        }

        # Utilizar la función realizar_transaccion
        _, mensaje, status_code = realizar_transaccion(cliente_id, transaccion_cancelacion)

        if status_code != 200:
            return None, mensaje, status_code

    # Actualizar el cliente en DynamoDB después de cancelar todas las suscripciones
    update_expression = "SET fondosSuscritos = :fondosSuscritos, saldoActual = :saldoActual"
    expression_attribute_values = {
        ':fondosSuscritos': cliente["fondosSuscritos"],
        ':saldoActual': cliente["saldoActual"]
    }

    try:
        update_cliente(cliente_id, update_expression, expression_attribute_values)
    except Exception as e:
        print(f'Error al actualizar el cliente: {str(e)}')
        return None, f'Error al actualizar el cliente: {str(e)}', 500

    return get_cliente(cliente_id), 'Fondos cancelados correctamente', 200

"""

# Función para obtener el historial de transacciones de un cliente

def obtener_historial_transacciones(cliente_id):
    # Obtener el cliente desde DynamoDB
    table_clientes = dynamodb.Table(TABLE_NAME_CLIENTES)
    response = table_clientes.get_item(Key={'Id': cliente_id})
    cliente = response.get('Item')

    if not cliente:
        return None  # Retorna None si el cliente no existe

    # Preparar el historial de transacciones
    historial_transacciones = []
    for transaccion in cliente.get('historialTransacciones', []):
        historial_transacciones.append({
            'fondoId': transaccion['fondoId'],
            'tipo': transaccion['tipo'],
            'monto': transaccion['monto'],
            'fecha': transaccion['fecha']
        })

    return historial_transacciones



def get_cliente_por_identificacion(numero_identificacion):
    try:
        table_clientes = dynamodb.Table(TABLE_NAME_CLIENTES)
        index_name = 'NumeroIdentificacionIndex'  # Reemplaza con el nombre real de tu índice global

        response = table_clientes.query(
            IndexName=index_name,
            KeyConditionExpression=Key('numeroIdentificacion').eq(numero_identificacion)
        )
        
        items = response.get('Items', [])
        
        if not items:
            return None
        
        return items[0]
    
    except Exception as e:
        print(f'Error al buscar cliente por identificación: {str(e)}')
        return None

def get_cliente_por_id(cliente_id):
    try:
        table_clientes = dynamodb.Table(TABLE_NAME_CLIENTES)

        # Obtener el cliente desde DynamoDB
        response = table_clientes.get_item(Key={'Id': cliente_id})
        cliente = response.get('Item')

        if not cliente:
            return {'mensaje': 'Cliente no encontrado'}, 404

        # Obtener historial de transacciones del cliente
        historial_transacciones = cliente.get('historialTransacciones', [])

        return {'cliente': cliente, 'historialTransacciones': historial_transacciones}, 200

    except Exception as e:
        return {'mensaje': f'Error al listar transacciones del cliente: {str(e)}'}, 500


def get_todas_las_transacciones():
    try:
        table_clientes = dynamodb.Table(TABLE_NAME_CLIENTES)

        response = table_clientes.scan()
        items = response.get('Items', [])

        todas_las_transacciones = []
        for item in items:
            cliente_id = item.get('Id', None)
            nombre_cliente = f"{item.get('Nombres', '')} {item.get('Apellidos', '')}".strip()
            historial_transacciones = item.get('historialTransacciones', [])

            for transaccion in historial_transacciones:
                transaccion_info = {
                    'transactionId': transaccion.get('transactionId', None),
                    'fondoId': transaccion.get('fondoId', None),
                    'tipo': transaccion.get('tipo', None),
                    'monto': transaccion.get('monto', None),
                    'fecha': transaccion.get('fecha', None)
                }
                todas_las_transacciones.append({
                    'clienteId': cliente_id,
                    'nombreCliente': nombre_cliente,
                    'transaccion': transaccion_info
                })

        return todas_las_transacciones

    except Exception as e:
        print(f'Error al obtener todas las transacciones: {str(e)}')
        return []


def enviar_correo(destinatario, asunto, cuerpo):
    ses = boto3.client('ses', region_name='us-west-2') 
    try:
        response = ses.send_email(
            Source='tu_correo@dominio.com', 
            Destination={
                'ToAddresses': [destinatario],
            },
            Message={
                'Subject': {
                    'Data': asunto,
                },
                'Body': {
                    'Text': {
                        'Data': cuerpo,
                    },
                },
            },
        )
    except ClientError as e:
        print(f'Error al enviar correo: {e.response["Error"]["Message"]}')
        return False
    return True

def enviar_sms(numero_telefono, mensaje):
    sns = boto3.client('sns', region_name='us-west-2')  
    try:
        response = sns.publish(
            PhoneNumber=numero_telefono,
            Message=mensaje,
        )
    except ClientError as e:
        print(f'Error al enviar SMS: {e.response["Error"]["Message"]}')
        return False
    return True


def enviar_correo(destinatario, asunto, cuerpo):
    ses = boto3.client('ses', region_name='us-east-1')  # Ajusta la región según tu configuración
    try:
        response = ses.send_email(
            Source='tu_correo@dominio.com',  # Reemplaza con tu dirección de correo verificada en SES
            Destination={
                'ToAddresses': [destinatario],
            },
            Message={
                'Subject': {
                    'Data': asunto,
                },
                'Body': {
                    'Text': {
                        'Data': cuerpo,
                    },
                },
            },
        )
    except ClientError as e:
        print(f'Error al enviar correo: {e.response["Error"]["Message"]}')
        return False
    return True

def enviar_sms(numero_telefono, mensaje):
    sns = boto3.client('sns', region_name='us-east-1')  # Ajusta la región según tu configuración
    try:
        response = sns.publish(
            PhoneNumber=numero_telefono,
            Message=mensaje,
        )
    except ClientError as e:
        print(f'Error al enviar SMS: {e.response["Error"]["Message"]}')
        return False
    return True


def realizar_transaccion(cliente_id, transaccion):
    tipo_transaccion = transaccion.get('tipo')
    monto = transaccion.get('monto')
    fondo_id = transaccion.get('fondoId')
    fecha = transaccion.get('fecha')

    table_clientes = dynamodb.Table(TABLE_NAME_CLIENTES)

    # Obtener el cliente
    response = table_clientes.get_item(Key={'Id': cliente_id})
    cliente = response.get('Item')

    if not cliente:
        return None, 'Cliente no encontrado', 404

    # Actualizar historial de transacciones
    historial_transacciones = cliente.get('historialTransacciones', [])
    nueva_transaccion = {
        'transactionId':  str(uuid4()),  # Generación de un ID único para la transacción
        'fondoId': fondo_id,
        'tipo': tipo_transaccion,
        'monto': monto,
        'fecha': fecha
    }
    historial_transacciones.append(nueva_transaccion)

    # Guardar la transacción en DynamoDB
    cliente['historialTransacciones'] = historial_transacciones
    table_clientes.put_item(Item=cliente)

    # Enviar notificación según preferencia
    preferencia_notificacion = cliente.get('preferenciaNotificacion')
    nombre_cliente = f"{cliente.get('Nombres', '')} {cliente.get('Apellidos', '')}".strip()
    mensaje = f"Hola {nombre_cliente}, se ha realizado una transacción de tipo {tipo_transaccion} por un monto de {monto}."

    if preferencia_notificacion == 'email':
        destinatario = cliente.get('Email')
        if destinatario:
            # Simular enviar correo, aquí deberías implementar tu lógica de envío de correo
            print(f"Enviando correo a {destinatario}: {mensaje}")
    elif preferencia_notificacion == 'sms':
        numero_telefono = cliente.get('Telefono')
        if numero_telefono:
            # Simular enviar SMS, aquí deberías implementar tu lógica de envío de SMS
            print(f"Enviando SMS a {numero_telefono}: {mensaje}")

    return cliente, 'Transacción realizada y notificación enviada.', 200


