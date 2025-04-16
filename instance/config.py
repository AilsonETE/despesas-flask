import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'sua-chave-secreta'
SQLALCHEMY_DATABASE_URI = 'sqlite:///despesas.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = os.path.join(BASE_DIR, '../app/static/uploads')
