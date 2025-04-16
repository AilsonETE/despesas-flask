from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    

class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    valor = db.Column(db.Float)
    data_vencimento = db.Column(db.Date)
    data_execucao = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20))  # "Executada" ou "Pendente"
    destino = db.Column(db.String(100))
    comprovante = db.Column(db.String(200))  # nome do arquivo
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
