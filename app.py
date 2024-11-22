from flask import Flask, request, jsonify
import logging
from token_service import TokenService, Unauthorized
from config import API_HOST, API_PORT

app = Flask(__name__)

# Instancia del servicio de autenticación
auth_service = TokenService()

@app.route('/token', methods=['PUT'])
def create_token():
    data = request.get_json()

    # Validación de entrada
    username = data.get("username")
    pass_hash = data.get("pass_hash")
    expiration_cb = data.get("expiration_cb")  # Expiración opcional del token

    if not username or not pass_hash:
        return jsonify({"error": "Bad Request: 'username' and 'pass_hash' are required."}), 400

    try:
        # Crear el token a través del servicio de autenticación
        token, live_time = auth_service.create_token(username, pass_hash, expiration_cb)
        # Devuelve el token y el tiempo de vida en segundos
        return jsonify({"token": token, "live_time": live_time}), 201
    except Exception as e:
        logging.error(f"Error creating token: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/token/<token>', methods=['DELETE'])

def revoke_token(token):
    """Revocar un token (eliminación)"""
    try:
        # Revocar el token solo si el propietario es el mismo que el proporcionado en la cabecera
        owner = request.headers.get('Owner')
        auth_service.revoke_token(token, owner)
        return '', 204  # No content
    except Unauthorized:
        return jsonify({"error": "Unauthorized: You are not the owner of this token."}), 401

@app.route('/token/<token>', methods=['GET'])
def get_token_info(token):
    """Obtener información sobre un token"""
    owner = request.headers.get('Owner')
    if not owner:
        return jsonify({"error": "Unauthorized: Owner header is missing"}), 401

    try:
        # Primero verificamos si el token existe
        token_info = auth_service.get_token_info(token)

        # Si el token existe, verificamos si el propietario coincide
        if token_info['username'] != owner:
            return jsonify({"error": "Unauthorized: You are not the owner of this token."}), 401

        return jsonify({"username": token_info['username'], "roles": token_info['roles']}), 200
    except Unauthorized:
        return jsonify({"error": "Unauthorized: You are not the owner of this token."}), 401

@app.before_first_request
def check_expired_tokens():
    """Revocar los tokens expirados antes de la primera solicitud"""
    auth_service.check_and_revoke_expired_tokens()

if __name__ == '__main__':
    # Ejecutar la aplicación Flask en el host y puerto configurado
    app.run(debug=True, host=API_HOST, port=API_PORT)

