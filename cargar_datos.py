from app import create_app
from config.database import db

from app.models.rol import Rol
from app.models.usuario import Usuario

from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    # ==========================
    # CREAR ROLES
    # ==========================
    if not Rol.query.first():

        administrador = Rol(
            nombre="Administrador"
        )

        docente = Rol(
            nombre="Docente"
        )

        estudiante = Rol(
            nombre="Estudiante"
        )

        db.session.add_all([
            administrador,
            docente,
            estudiante
        ])

        db.session.commit()

        print(
            "Roles creados correctamente."
        )

    else:

        print(
            "Los roles ya existen."
        )

    # ==========================
    # CREAR ADMINISTRADOR
    # ==========================
    admin = Usuario.query.filter_by(
        correo="admin@ues.edu.sv"
    ).first()

    if not admin:

        admin = Usuario(
            nombre="Administrador",
            correo="admin@ues.edu.sv",
            password=generate_password_hash(
                "admin123"
            ),
            rol_id=Rol.query.filter_by(
                nombre="Administrador"
            ).first().id
        )

        db.session.add(
            admin
        )

        db.session.commit()

        print(
            "Administrador creado correctamente."
        )

    else:

        print(
            "El administrador ya existe."
        )

    # ==========================
    # CREAR DOCENTE
    # ==========================
    docente = Usuario.query.filter_by(
        correo="docente@ues.edu.sv"
    ).first()

    if not docente:

        docente = Usuario(
            nombre="Docente",
            correo="docente@ues.edu.sv",
            password=generate_password_hash(
                "docente123"
            ),
            rol_id=Rol.query.filter_by(
                nombre="Docente"
            ).first().id
        )

        db.session.add(
            docente
        )

        db.session.commit()

        print(
            "Docente creado correctamente."
        )

    else:

        print(
            "El docente ya existe."
        )

print(
    "Proceso completado."
)