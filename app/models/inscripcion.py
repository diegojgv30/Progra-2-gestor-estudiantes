from config.database import db

class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    asignatura_id = db.Column(db.Integer, db.ForeignKey('asignaturas.id'), nullable=False)
    
    # Relaciones
    estudiante = db.relationship('Estudiante', backref='inscripciones')
    asignatura = db.relationship('Asignatura', backref='inscripciones')