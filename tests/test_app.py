import json
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
class TestApp(unittest.TestCase):
    def setUp(self):
        """Configurar el entorno de prueba, incluyendo la creación de un token"""
        self.app = app.test_client()
        self.username = "testuser"
        self.pass_hash = "hashed_password"  # Usar un hash adecuado en un caso real
        self.expiration_cb = None
        
        # Crear un token usando la API
        response = self.app.put('/token', json={
            "username": self.username,
            "pass_hash": self.pass_hash,
            "expiration_cb": self.expiration_cb
        })
        
        # Asegurarse de que la creación del token fue exitosa
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.token = data['token']  # Guardar el token para pruebas posteriores

    def test_get_token_info(self):
        """Probar el método GET para obtener la información de un token"""
        # Usar el token creado en el setUp
        response = self.app.get(f'/token/{self.token}', headers={'Owner': self.username})
        data = json.loads(response.data)

        # Verificar si la respuesta tiene un código de estado 200 y si los datos son correctos
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['username'], self.username)

    def test_get_token_info_unauthorized(self):
        """Probar el método GET cuando el propietario es incorrecto"""
        # Intentar obtener la información del token con un propietario incorrecto
        response = self.app.get(f'/token/{self.token}', headers={'Owner': 'wronguser'})
        data = json.loads(response.data)

        # Verificar si la respuesta es 401 Unauthorized
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], "Unauthorized: You are not the owner of this token.")

    def test_revoke_token_success(self):
        """Probar el método DELETE para revocar un token exitosamente"""
        # Usar el token creado en el setUp
        response = self.app.delete(f'/token/{self.token}', headers={'Owner': self.username})
        
        # Verificar si la respuesta es 204 (No Content) y que el token fue revocado
        self.assertEqual(response.status_code, 204)

        # Intentar obtener la información del token después de revocarlo (debe fallar)
        response = self.app.get(f'/token/{self.token}', headers={'Owner': self.username})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], "Unauthorized: You are not the owner of this token.")

    def test_revoke_token_unauthorized(self):
        """Probar el método DELETE cuando el propietario no coincide con el token"""
        # Intentar revocar el token con un propietario incorrecto
        response = self.app.delete(f'/token/{self.token}', headers={'Owner': 'wronguser'})

        # Verificar si la respuesta es 401 Unauthorized
        data = json.loads(response.data)  # Intentar cargar la respuesta como JSON
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], "Unauthorized: You are not the owner of this token.")

if __name__ == '__main__':
    unittest.main()

