# adi1

Ahora para ejecutar el proyecto utlizaremos docker, en primer lugar tenemos que dar permiso de ejecución a los tres scripsts.

```bash
chomod +x build run stop
```

A continuación construimos la imagen de docker:

```bash
sudo ./build
```

Y ya podremos lanzar el servicio:

```bash
sudo ./run
```

Si queremos finalizar el servicio tan solo deberemos ejecutar:

```bash
sudo ./run
```

Podemos comproabr el funcionamiento del servicio mediante client.py que ejecutatara las tres operaciones(PUT,GET y DELETE):

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


