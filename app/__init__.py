from flask import Flask
from flask_login import LoginManager

from config.database import db
from config.settings import Config


login_manager = LoginManager()

login_manager.login_view = "auth.login"

login_manager.login_message = (
    "Por favor, inicia sesión para acceder a esta página."
)

login_manager.login_message_category = "info"


def create_app():

    app = Flask(__name__)

    app.config.from_object(
        Config
    )

    db.init_app(
        app
    )

    login_manager.init_app(
        app
    )

    @login_manager.user_loader
    def load_user(user_id):

        from app.models.usuario import Usuario

        return Usuario.query.get(
            int(user_id)
        )

    with app.app_context():

        from app.models.rol import Rol
        from app.models.usuario import Usuario
        from app.models.estudiante import Estudiante
        from app.models.asignatura import Asignatura
        from app.models.inscripcion import Inscripcion
        from app.models.calificacion import Calificacion

    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(
        auth_bp
    )

    from app.controllers.estudiante_controller import estudiantes_bp

    app.register_blueprint(
        estudiantes_bp,
        url_prefix='/estudiantes'
    )

    from app.controllers.asignatura_controller import asignaturas_bp

    app.register_blueprint(
        asignaturas_bp,
        url_prefix='/asignaturas'
    )

    from app.controllers.inscripcion_controller import inscripciones_bp

    app.register_blueprint(
        inscripciones_bp,
        url_prefix='/inscripciones'
    )

    from app.controllers.calificaciones_controller import calificaciones_bp

    app.register_blueprint(
        calificaciones_bp,
        url_prefix='/calificaciones'
    )

    return app