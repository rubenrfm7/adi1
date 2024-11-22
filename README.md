# adi1

Para ejecutar el proyecto, en primero lugar es recomendable crear un entorno virtual.

```bash
python3 -m venv venv
source venv/bin/activate  # En sistemas Unix (Linux/MacOS)
venv\Scripts\activate     # En Windows
```

A continuación intalamos los requisitos:

```bash
pip install requirements.txt
```

Ya podremos lanzar el servidor:

```bash
python app.py
```

He creado un cliente para probar las tres funcionalidades de la API(PUT,GET y DELETE):

```bash
python client.py
```

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
 #Pruebas

 He realizado las pruebas con las herramientas pytest y coverage.

 Con pytest he realizado el testeo de de la capa de presentación y de negocio:

 ```
pytest tests/
```

Y con coverage he comprobado el grado de cobertura de estas pruebas y lo he exportado a html.

```
coverage run -m unittest discover tests/
coverge html
```

Dando como resultado lo siguiente:

![Captura desde 2024-11-22 12-56-22](https://github.com/user-attachments/assets/b672ad17-0306-4242-8b08-f5853e063330)


