from config.database import db

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    inscripcion_id = db.Column(db.Integer, db.ForeignKey('inscripciones.id'), nullable=False)
    
    # Usamos comillas para evitar el error de "failed to locate a name"
    inscripcion = db.relationship('Inscripcion', backref='calificaciones')

    def __init__(self, nota, inscripcion_id):
        self.nota = nota
        self.inscripcion_id = inscripcion_id