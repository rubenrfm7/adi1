import requests

class AuthClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_token(self, username, pass_hash, expiration_cb=None):
        url = f"{self.base_url}/token"
        data = {
            "username": username,
            "pass_hash": pass_hash,
            "expiration_cb": expiration_cb
        }
        response = requests.put(url, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            return response.json()

    def revoke_token(self, token, owner):
        url = f"{self.base_url}/token/{token}"
        headers = {"Owner": owner}
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return "Token revoked successfully"
        else:
            return response.json()

    def get_token_info(self, token,owner):
        url = f"{self.base_url}/token/{token}"
        headers = {"Owner": owner}
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()

# Uso del cliente
client = AuthClient("http://localhost:3002")
# Crear un token
token_data = client.create_token("user1", "password_hash")
print("Token creado:", token_data)

# Obtener la información del token (con propietario)
get_data = client.get_token_info(token_data['token'],"user1")
print("Información del token:", get_data)

# Revocar el token
revoke_data = client.revoke_token(token_data['token'], "user1")
print(revoke_data)

# Intentar obtener la información del token después de revocar (debe fallar)
get_data_after_revoke = client.get_token_info(token_data['token'],"user1")
print("Información del token después de revocar:", get_data_after_revoke)
