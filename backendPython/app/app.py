# app/app.py
from flask import jsonify, request
from flask_cors import CORS

from services import add_fondo_suscrito, cancelar_suscripcion, obtener_historial_transacciones, get_cliente_por_identificacion,  get_cliente_por_id, get_todas_las_transacciones
#, get_fondo

from models import add_cliente, get_cliente, update_cliente, delete_cliente, add_transaccion, add_fondo, get_fondos, get_fondo,create_tables
from uuid import uuid4
from datetime import datetime
from flask import Flask
#from routes import app as routes_bp

app = Flask(__name__)
#app.register_blueprint(routes_bp)

CORS(app)  # Activa CORS en todos los endpoints

# Definiciones de URL
@app.route('/')
def index():
    return "¡Bienvenido a la API Backend!"


@app.route('/clientes', methods=['POST'])
def route_crear_cliente():
    cliente = request.json
    cliente["Id"] = str(uuid4())  # Generar un UUID único para el cliente
    cliente["fondosSuscritos"] = []
    cliente["historialTransacciones"] = []
    add_cliente(cliente)
    return jsonify(cliente), 201  



@app.route('/clientes/<string:cliente_id>', methods=['GET'])
def route_obtener_cliente(cliente_id):
    cliente = get_cliente(cliente_id)
    if cliente:
        return jsonify(cliente), 200
    else:
        return jsonify({"message": "Cliente no encontrado"}), 404
 
    
@app.route('/clientes/<cliente_id>', methods=['PUT'])
def route_actualizar_cliente(cliente_id):
    update_expression = "SET Nombres = :n, Apellidos = :a, Email = :e, Telefono = :t, saldoActual = :s, preferenciaNotificacion = :p"
    expression_attribute_values = {
        ':n': request.json.get('Nombres'),
        ':a': request.json.get('Apellidos'),
        ':e': request.json.get('Email'),
        ':t': request.json.get('Telefono'),
        ':s': request.json.get('saldoActual'),
        ':p': request.json.get('preferenciaNotificacion')
    }
    update_cliente(cliente_id, update_expression, expression_attribute_values)
    return jsonify({"message": "Cliente actualizado exitosamente"}), 200

@app.route('/clientes/<cliente_id>', methods=['DELETE'])
def route_eliminar_cliente(cliente_id):
    delete_cliente(cliente_id)
    return jsonify({"message": "Cliente eliminado exitosamente"}), 200

@app.route('/fondos', methods=['POST'])
def route_crear_fondo():
    fondo = request.json
    fondo["fondoId"] = str(uuid4())  # Generar un UUID único para el fondo
    add_fondo(fondo)
    return jsonify(fondo), 201

    
@app.route('/fondos', methods=['GET'])
def route_obtener_fondos():
    fondos = get_fondos()
    return jsonify(fondos), 200

@app.route('/fondos/<fondo_id>', methods=['GET'])
def route_obtener_fondo(fondo_id):
    fondo = get_fondo(fondo_id)
    if fondo:
        return jsonify(fondo), 200
    else:
        return jsonify({"message": "Fondo no encontrado"}), 404

#Agrear suscripcion fondos
@app.route('/clientes/<cliente_id>/fondos', methods=['POST'])
def route_suscribir_fondo(cliente_id):
    print(f'Entre a funcion route_suscribir_fondo')

    fondos = request.json

    cliente_actualizado = add_fondo_suscrito(cliente_id, fondos)

    if cliente_actualizado:
        
        return jsonify(cliente_actualizado), 200
    else:
        return jsonify({"message": "Cliente no encontrado"}), 404


# Cancelar suscripciones a varios fondos de un cliente
@app.route('/clientes/<cliente_id>/cancelar_suscripciones', methods=['POST'])
def route_cancelar_suscripciones(cliente_id):
    data = request.json
    fondos_a_cancelar = data.get('fondos_a_cancelar', [])

    cliente_actualizado = cancelar_suscripcion(cliente_id, fondos_a_cancelar)
    
    if cliente_actualizado:
        return jsonify(cliente_actualizado), 200
    else:
        return jsonify({"message": "Cliente no encontrado"}), 404


@app.route('/clientes/buscar/<numero_identificacion>', methods=['GET'])
def route_buscar_cliente(numero_identificacion):
     # Eliminar espacios en blanco del número de identificación
    numero_identificacion = numero_identificacion.strip()

    cliente = get_cliente_por_identificacion(numero_identificacion)
    
    if not cliente:
        return jsonify({'mensaje': 'Cliente no encontrado'}), 404
    
    return jsonify(cliente), 200

#Historial de transacciones por cliente
@app.route('/clientes/<cliente_id>/transacciones', methods=['GET'])
def route_listar_transacciones_cliente(cliente_id):
    # Obtener el historial de transacciones del cliente usando la función
    historial_transacciones = obtener_historial_transacciones(cliente_id)

    if not historial_transacciones:
        return jsonify({'mensaje': 'Cliente no encontrado o sin historial de transacciones'}), 404

    return jsonify({'historialTransacciones': historial_transacciones}), 200



#actualizar transacion
@app.route('/clientes/<cliente_id>/transacciones/<transaction_id>', methods=['PUT'])
def route_actualizar_transaccion_cliente(cliente_id, transaction_id):
    cliente = get_cliente_por_id(cliente_id)
    
    if not cliente:
        return jsonify({'mensaje': 'Cliente no encontrado'}), 404
    
    data = request.json
    
    # Buscar la transacción por transaction_id en el historial del cliente
    transaccion_encontrada = None
    for transaccion in cliente.get('historialTransacciones', []):
        if transaccion['transactionId'] == transaction_id:
            transaccion_encontrada = transaccion
            break
    
    if not transaccion_encontrada:
        return jsonify({'mensaje': 'Transacción no encontrada'}), 404
    
    # Actualizar los campos de la transacción encontrada
    transaccion_encontrada['fondoId'] = data.get('fondoId', transaccion_encontrada['fondoId'])
    transaccion_encontrada['tipo'] = data.get('tipo', transaccion_encontrada['tipo'])
    transaccion_encontrada['monto'] = data.get('monto', transaccion_encontrada['monto'])
    transaccion_encontrada['fecha'] = datetime.utcnow().isoformat()
    
    # actualizar db
    
    return jsonify({'mensaje': 'Transacción actualizada correctamente'}), 200


@app.route('/clientes/<cliente_id>/transacciones/<transaction_id>', methods=['DELETE'])
def route_eliminar_transaccion_cliente(cliente_id, transaction_id):
    cliente = get_cliente_por_id(cliente_id)
    
    if not cliente:
        return jsonify({'mensaje': 'Cliente no encontrado'}), 404
    
    # Buscar la transacción por transaction_id en el historial del cliente
    transaccion_encontrada = None
    for transaccion in cliente.get('historialTransacciones', []):
        if transaccion['transactionId'] == transaction_id:
            transaccion_encontrada = transaccion
            break
    
    if not transaccion_encontrada:
        return jsonify({'mensaje': 'Transacción no encontrada'}), 404
    
    # Eliminar la transacción del historial del cliente
    cliente['historialTransacciones'].remove(transaccion_encontrada)
    
    # actualizar db
    
    return jsonify({'mensaje': 'Transacción eliminada correctamente'}), 200

# Para listar todas las transacciones
@app.route('/clientes/transacciones', methods=['GET'])
def route_listar_todas_transacciones():
    try:
        todas_las_transacciones = get_todas_las_transacciones()

        if not todas_las_transacciones:
            return jsonify({'mensaje': 'No se encontraron transacciones'}), 404

        transacciones = []
        for transaccion in todas_las_transacciones:
            transacciones.append({
                'clienteId': transaccion.get('clienteId'),
                'nombreCliente': transaccion.get('nombreCliente'),
                'transaccion': transaccion.get('transaccion')
            })

        return jsonify({'transacciones': transacciones}), 200

    except Exception as e:
        return jsonify({'mensaje': f'Error al obtener las transacciones: {str(e)}'}), 500


if __name__ == '__main__':
    create_tables()  # Llama a create_table() al iniciar la aplicación
    app.run(debug=True)

