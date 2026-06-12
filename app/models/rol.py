from config.database import db

class Rol(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relación para saber qué usuarios tienen este rol
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)