# Python base slim (más ligero)
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar requirements primero para mejor cache
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente y configuración
COPY src/ ./src/
COPY config/ ./config/

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Crear directorios para datos
RUN mkdir -p /app/data/audio/uploads /app/data/audio/samples /app/data/transcriptions/output

# Exponer puerto para API
EXPOSE 8000

# Comando por defecto - servidor API
CMD ["python", "src/api_server.py"]