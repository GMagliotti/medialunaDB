FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Copiar el Pipfile y Pipfile.lock
COPY Pipfile /app/

# Instalar Pipenv y dependencias del proyecto
ENV PATH ${HOME}/app/.local/bin:${PATH}

RUN pip install pipenv && pipenv install

COPY . /app

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
ENTRYPOINT ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
