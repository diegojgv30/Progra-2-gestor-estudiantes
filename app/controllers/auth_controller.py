from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    check_password_hash
)

from app.models.usuario import Usuario
from app.models import (
    Estudiante,
    Asignatura,
    Calificacion,
    Inscripcion
)

from app.forms.auth_form import LoginForm


auth_bp = Blueprint(
    'auth',
    __name__
)


@auth_bp.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for(
                'auth.dashboard'
            )
        )

    form = LoginForm()

    if form.validate_on_submit():

        usuario = Usuario.query.filter_by(
            correo=form.correo.data
        ).first()

        if (
            usuario and
            check_password_hash(
                usuario.password,
                form.password.data
            )
        ):

            if not usuario.activo:

                flash(
                    'Esta cuenta está desactivada.',
                    'danger'
                )

                return redirect(
                    url_for(
                        'auth.login'
                    )
                )

            login_user(
                usuario,
                remember=form.recordarme.data
            )

            flash(
                f'¡Bienvenido/a {usuario.nombre}!',
                'success'
            )

            next_page = request.args.get(
                'next'
            )

            return redirect(
                next_page
            ) if next_page else redirect(
                url_for(
                    'auth.dashboard'
                )
            )

        flash(
            'Correo o contraseña incorrectos.',
            'danger'
        )

    return render_template(
        'auth/login.html',
        form=form
    )


@auth_bp.route(
    '/dashboard'
)
@login_required
def dashboard():

    rol = current_user.rol.nombre

    datos = {}

    if rol == 'Administrador':

        datos = {

            'estudiantes':
            Estudiante.query.count(),

            'docentes':
            Usuario.query.join(
                Usuario.rol
            ).filter(
                Usuario.rol.has(
                    nombre='Docente'
                )
            ).count(),

            'asignaturas':
            Asignatura.query.count(),

            'inscripciones':
            Inscripcion.query.count(),

            'calificaciones':
            Calificacion.query.count()
        }

    elif rol == 'Docente':

        datos = {

            'estudiantes':
            Estudiante.query.count(),

            'asignaturas':
            Asignatura.query.count(),

            'calificaciones':
            Calificacion.query.count()
        }

    elif rol == 'Estudiante':

        estudiante = (
            current_user.estudiante
        )

        inscripciones = (
            estudiante.inscripciones
            if estudiante
            else []
        )

        calificaciones = []

        for inscripcion in inscripciones:

            calificaciones.extend(
                inscripcion.calificaciones
            )

        aprobadas = len(
            [
                c for c in calificaciones
                if c.nota >= 6
            ]
        )

        reprobadas = len(
            [
                c for c in calificaciones
                if c.nota < 6
            ]
        )

        promedio = 0

        if calificaciones:

            promedio = round(
                sum(
                    c.nota
                    for c in calificaciones
                ) /
                len(
                    calificaciones
                ),
                2
            )

        datos = {

            'materias':
            len(inscripciones),

            'aprobadas':
            aprobadas,

            'reprobadas':
            reprobadas,

            'promedio':
            promedio
        }

    return render_template(
        'auth/dashboard.html',
        datos=datos,
        rol=rol
    )


@auth_bp.route(
    '/logout'
)
@login_required
def logout():

    logout_user()

    flash(
        'Has cerrado sesión correctamente.',
        'success'
    )

    return redirect(
        url_for(
            'auth.login'
        )
    )


@auth_bp.route('/')
def index():

    if current_user.is_authenticated:

        return redirect(
            url_for(
                'auth.dashboard'
            )
        )

    return redirect(
        url_for(
            'auth.login'
        )
    )