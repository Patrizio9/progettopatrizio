# Usa una base image di Python per Flask
FROM python:3.9-slim

# Imposta il working directory nel container
WORKDIR /app

# Copia i file necessari nel container
COPY app.py /app
COPY templates /app/templates

# Installa le dipendenze necessarie
RUN pip install Flask mysql-connector-python


# Comando per eseguire l'applicazione Flask
CMD ["python", "app.py"]
