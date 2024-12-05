# Usar una imagen ligera de Python
FROM python:3.11-slim

# Crear un usuario no-root
RUN addgroup --system appgroup && adduser --system --group appuser

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Cambiar a un usuario no-root
USER appuser

# Exponer el puerto del servicio
EXPOSE 3002

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
