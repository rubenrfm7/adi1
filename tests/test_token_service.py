import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from token_service import TokenService, Unauthorized
from unittest.mock import patch,MagicMock
import time


class TestAuthService(unittest.TestCase):
    def setUp(self):
        """Configuración inicial de la prueba"""
        self.auth_service = TokenService()
        self.username = 'testuser'
        self.pass_hash = 'hashed_password'
        self.token = self.auth_service.create_token(self.username, self.pass_hash)[0]

    
    @patch('requests.put')  # Mock de requests.put
    @patch('time.time', return_value=1000)  # Mock de time.time()
    @patch('logging.info')  # Mock de logging.info
    def test_schedule_expiration_callback_function(self, mock_info, mock_time, mock_put):
        """Verifica el flujo cuando expiration_cb es una función callable."""
        auth_service = TokenService()
        
        # Definir una función de callback simulada
        def mock_callback():
            pass

        # Simular la creación de un token con un callback como función
        token = "test_token"
        expiration_cb = mock_callback

        # Llamar al método que queremos probar
        auth_service.schedule_expiration_callback(expiration_cb, 4600)
    
        # Verificar que la información de la programación fue registrada
        mock_info.assert_called_with(f"Scheduling expiration callback for {mock_callback} at 4600")
        # Verificar que la función de callback fue llamada
        

    @patch('requests.put')  # Mock de requests.put
    @patch('time.time', return_value=1000)  # Mock de time.time()
    @patch('logging.info')  # Mock de logging.info
    def test_schedule_expiration_callback_url(self, mock_info, mock_time, mock_put):
        """Verifica el flujo cuando expiration_cb es una URL."""
        auth_service = TokenService()

        # Simular que expiration_cb es una URL
        expiration_cb = "http://dummy-url.com/callback"
        token = "test_token"
        
        # Configuramos el mock de requests.put para que devuelva un código 200
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        # Llamar al método que queremos probar
        auth_service.schedule_expiration_callback(expiration_cb,4600)

        # Verificar que la información de la programación fue registrada
        mock_info.assert_called_with(f"Scheduling expiration callback for {expiration_cb} at 4600")

    @patch('requests.put')  # Mock de requests.put
    @patch('time.time', return_value=1000)  # Mock de time.time()
    @patch('logging.info')  # Mock de logging.info
    @patch('logging.error')  # Mock de logging.error
    def test_schedule_expiration_callback_error(self, mock_error, mock_info, mock_time, mock_put):
        """Verifica que el manejo de errores funciona cuando ocurre una excepción."""
        auth_service = TokenService()

        # Simular que expiration_cb es una URL
        expiration_cb = "http://dummy-url.com/callback"
        token = "test_token"

        # Configuramos el mock de requests.put para que lance una excepción
        mock_put.side_effect = Exception("Request failed")

        # Llamar al método que queremos probar
        auth_service.schedule_expiration_callback(token, expiration_cb)

        # Verificar que se registró un error
        mock_error.assert_called_with("Error while calling expiration callback for token: Request failed")

    @patch.object(TokenService, 'create_token')   
    def test_create_token_success(self, mock_create_token):
        # Simulando que el método 'create_token' retorna un token con un tiempo de vida
        mock_create_token.return_value = ('test-token', 3600)
        
        auth_service = TokenService()
        token, live_time = auth_service.create_token('testuser', 'hashedpassword')

        self.assertEqual(token, 'test-token')
        self.assertEqual(live_time, 3600)
    
    @patch.object(TokenService, 'get_token_info')
    def test_get_token_info_success(self, mock_get_token_info):
        # Simulando que el método 'get_token_info' devuelve un diccionario con la info del token
        mock_get_token_info.return_value = {'username': 'testuser', 'roles': ['admin']}
        
        auth_service = TokenService()
        token_info = auth_service.get_token_info('test-token')

        self.assertEqual(token_info['username'], 'testuser')
        self.assertIn('admin', token_info['roles'])
    
    @patch.object(TokenService, 'revoke_token')
    def test_revoke_token_success(self, mock_revoke_token):
        # Simulando que el método 'revoke_token' no lanza excepciones
        auth_service = TokenService()
        try:
            auth_service.revoke_token('test-token', 'testuser')
        except Unauthorized:
            self.fail("revoke_token() raised Unauthorized unexpectedly!")
    
    def test_Unauthorized(self):
        # Probar que se lanza la excepción correcta si el propietario no coincide
        auth_service = TokenService()
        with self.assertRaises(Unauthorized):
            auth_service.revoke_token('test-token', 'anotheruser')
            

if __name__ == '__main__':
    unittest.main()
