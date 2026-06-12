from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from werkzeug.security import generate_password_hash

from config.database import db

from app.models.estudiante import Estudiante
from app.models.usuario import Usuario
from app.models.rol import Rol

from app.forms.estudiante_form import EstudianteForm

from app.controllers.permisos import rol_requerido


estudiantes_bp = Blueprint(
    'estudiantes',
    __name__,
    url_prefix='/estudiantes'
)


@estudiantes_bp.route('/')
@login_required
@rol_requerido(
    "Administrador",
    "Docente"
)
def lista():

    form = EstudianteForm()

    busqueda = request.args.get(
        'buscar',
        ''
    ).strip()

    estudiantes_query = Estudiante.query

    if busqueda:

        estudiantes_query = estudiantes_query.filter(
            db.or_(
                Estudiante.carnet.ilike(
                    f'%{busqueda}%'
                ),
                Estudiante.nombres.ilike(
                    f'%{busqueda}%'
                ),
                Estudiante.apellidos.ilike(
                    f'%{busqueda}%'
                ),
                Estudiante.correo.ilike(
                    f'%{busqueda}%'
                )
            )
        )

    estudiantes = estudiantes_query.order_by(
        Estudiante.apellidos.asc()
    ).all()

    return render_template(
        'estudiantes/lista.html',
        estudiantes=estudiantes,
        form=form,
        busqueda=busqueda
    )


@estudiantes_bp.route(
    '/crear',
    methods=['POST']
)
@login_required
@rol_requerido(
    "Administrador"
)
def crear():

    form = EstudianteForm()

    if form.validate_on_submit():

        carnet = form.carnet.data.upper()
        correo = form.correo.data.strip().lower()

        existe_carnet = Estudiante.query.filter_by(
            carnet=carnet
        ).first()

        existe_correo_estudiante = Estudiante.query.filter_by(
            correo=correo
        ).first()

        existe_correo_usuario = Usuario.query.filter_by(
            correo=correo
        ).first()

        if existe_carnet:

            flash(
                'El carnet ingresado ya está registrado.',
                'danger'
            )

        elif existe_correo_estudiante or existe_correo_usuario:

            flash(
                'El correo electrónico ya está registrado.',
                'danger'
            )

        else:

            try:

                rol_estudiante = Rol.query.filter_by(
                    nombre="Estudiante"
                ).first()

                nuevo_usuario = Usuario(
                    nombre=f"{form.nombres.data} {form.apellidos.data}",
                    correo=correo,
                    password=generate_password_hash(
                        carnet
                    ),
                    rol_id=rol_estudiante.id
                )

                db.session.add(
                    nuevo_usuario
                )

                db.session.flush()

                nuevo_estudiante = Estudiante(
                    carnet=carnet,
                    nombres=form.nombres.data,
                    apellidos=form.apellidos.data,
                    correo=correo,
                    usuario_id=nuevo_usuario.id
                )

                db.session.add(
                    nuevo_estudiante
                )

                db.session.commit()

                flash(
                    f'Estudiante registrado exitosamente. Contraseña inicial: {carnet}',
                    'success'
                )

            except Exception as e:

                db.session.rollback()

                flash(
                    f'Error al registrar estudiante: {str(e)}',
                    'danger'
                )

    else:

        for field, errors in form.errors.items():

            for error in errors:

                flash(
                    f"Error en {getattr(form, field).label.text}: {error}",
                    'danger'
                )

    return redirect(
        url_for('estudiantes.lista')
    )


@estudiantes_bp.route(
    '/eliminar/<int:id>',
    methods=['POST']
)
@login_required
@rol_requerido(
    "Administrador"
)
def eliminar(id):

    estudiante = Estudiante.query.get_or_404(
        id
    )

    try:

        usuario = Usuario.query.get(
            estudiante.usuario_id
        )

        db.session.delete(
            estudiante
        )

        if usuario:

            db.session.delete(
                usuario
            )

        db.session.commit()

        flash(
            'Estudiante eliminado correctamente.',
            'success'
        )

    except Exception:

        db.session.rollback()

        flash(
            'No se puede eliminar el estudiante porque tiene inscripciones o notas asociadas.',
            'danger'
        )

    return redirect(
        url_for('estudiantes.lista')
    )


@estudiantes_bp.route(
    '/editar/<int:id>',
    methods=['GET', 'POST']
)
@login_required
@rol_requerido(
    "Administrador"
)
def editar(id):

    estudiante = Estudiante.query.get_or_404(
        id
    )

    form = EstudianteForm(
        obj=estudiante
    )

    if form.validate_on_submit():

        carnet = form.carnet.data.upper()
        correo = form.correo.data.strip().lower()

        choque_carnet = Estudiante.query.filter(
            Estudiante.carnet == carnet,
            Estudiante.id != id
        ).first()

        choque_correo = Estudiante.query.filter(
            Estudiante.correo == correo,
            Estudiante.id != id
        ).first()

        if choque_carnet:

            flash(
                'El carnet ingresado ya pertenece a otro estudiante.',
                'danger'
            )

            return render_template(
                'estudiantes/editar.html',
                form=form,
                estudiante=estudiante
            )

        if choque_correo:

            flash(
                'El correo electrónico ya pertenece a otro estudiante.',
                'danger'
            )

            return render_template(
                'estudiantes/editar.html',
                form=form,
                estudiante=estudiante
            )

        try:

            usuario = Usuario.query.get(
                estudiante.usuario_id
            )

            estudiante.carnet = carnet
            estudiante.nombres = form.nombres.data
            estudiante.apellidos = form.apellidos.data
            estudiante.correo = correo

            if usuario:

                usuario.nombre = (
                    f"{form.nombres.data} "
                    f"{form.apellidos.data}"
                )

                usuario.correo = correo

            db.session.commit()

            flash(
                'Estudiante actualizado exitosamente.',
                'success'
            )

            return redirect(
                url_for('estudiantes.lista')
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f'Error al actualizar estudiante: {str(e)}',
                'danger'
            )

    return render_template(
        'estudiantes/editar.html',
        form=form,
        estudiante=estudiante
    )