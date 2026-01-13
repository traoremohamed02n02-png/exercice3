# Image de base Python 3.8
FROM python:3.8

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier le contenu du dossier api/ dans /app du conteneur
COPY api/ .

# Installer Flask
RUN pip install flask

# Indiquer le port utilisé par Flask
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
