import time
import logging
import requests

# Excepciones

class Unauthorized(Exception):
    def __init__(self, token):
        self.token = token

# Clase que representa la capa de negocio
class TokenService:
    def __init__(self, callback_url=None):
        self.tokens = {}  # Diccionario para almacenar los tokens en memoria
        self.callback_url = callback_url  # URL del callback para la caducidad

    def create_token(self, username, pass_hash, expiration_cb=None):
        token = self.generate_token(username, pass_hash)  # Este es el token único generado
        expiration_time = time.time() + 3600  # 1 hora de validez por defecto
        self.tokens[token] = {
            'username': username,
            'pass_hash': pass_hash,
            'expiration_time': expiration_time,
            #Como no se indica el rol en ninguna cabecera, por defecto se crea el token solo para user.
            # if (role == 'admin'){
             #   roles : ['ADMIN']
            #}
            'roles': ['user'],
            'expiration_cb': expiration_cb  # Guardamos el callback correctamente
        }
        live_time = expiration_time - time.time()

        # Si se proporciona un callback de expiración, se realiza el PUT a la URL
        if expiration_cb:
            self.schedule_expiration_callback(expiration_cb, expiration_time)  # Pasamos correctamente el callback

        return token, int(live_time)


    def revoke_token(self, token, owner):
        if token not in self.tokens:
            raise Unauthorized(token)
        if self.tokens[token]['username'] != owner:
            raise Unauthorized(token) 
        del self.tokens[token] 

    def get_token_info(self, token):
        if token not in self.tokens:
            raise Unauthorized(token)
        return self.tokens[token]

    def check_and_revoke_expired_tokens(self):
        current_time = time.time()
        expired_tokens = [token for token, data in self.tokens.items() if data['expiration_time'] < current_time]

        for token in expired_tokens:
            self.revoke_token(token, self.tokens[token]['username'])

    def generate_token(self, username, pass_hash):
        # Generación simple de un token único. En un caso real, usar JWT o algo más seguro.
        return f"{username}_{pass_hash}_{int(time.time())}"

    def schedule_expiration_callback(self, expiration_cb, expiration_time):
        """Método para manejar la programación del callback de expiración"""
        try:
            # Aquí, en lugar de hacer un PUT con una URL, esperamos que `expiration_cb`
            # sea un nombre de función o un identificador que podamos usar.
            logging.info(f"Scheduling expiration callback for {expiration_cb} at {expiration_time}")
            # El callback puede ser simplemente invocado con los parámetros correspondientes
            if callable(expiration_cb):
                expiration_cb()
            else:
                # Si `expiration_cb` es una URL (o alguna cadena que indique un callback),
                # podríamos hacer una solicitud a ese endpoint
                response = requests.put(expiration_cb, json={"token": "dummy_token"})
                if response.status_code // 100 != 2:  # Verifica si la respuesta no es 2xx
                    logging.error(f"Failed to notify expiration callback for token with URL {expiration_cb}")
        except Exception as e:
            logging.error(f"Error while calling expiration callback for token: {e}")
