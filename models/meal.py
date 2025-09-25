from database import db
from flask_login import UserMixin
from datetime import datetime

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    dentro_da_dieta = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, nullable=False) 
