from config.database import db


class Estudiante(db.Model):

    __tablename__ = 'estudiantes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    carnet = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    nombres = db.Column(
        db.String(100),
        nullable=False
    )

    apellidos = db.Column(
        db.String(100),
        nullable=False
    )

    correo = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=True,
        unique=True
    )

    def __repr__(self):

        return (
            f"<Estudiante {self.carnet} - "
            f"{self.nombres} {self.apellidos}>"
        )