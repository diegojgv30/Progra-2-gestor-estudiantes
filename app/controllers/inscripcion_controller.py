from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from config.database import db

from app.models.inscripcion import Inscripcion
from app.models.estudiante import Estudiante
from app.models.asignatura import Asignatura

from app.forms.inscripcion_form import InscripcionForm

from app.controllers.permisos import rol_requerido


inscripciones_bp = Blueprint(
    'inscripciones',
    __name__,
    url_prefix='/inscripciones'
)


@inscripciones_bp.route('/')
@login_required
@rol_requerido(
    "Administrador",
    "Docente"
)
def lista():

    inscripciones = (
        Inscripcion.query
        .join(Estudiante)
        .join(Asignatura)
        .order_by(
            Estudiante.apellidos
        )
        .all()
    )

    form = InscripcionForm()

    form.estudiante_id.choices = [

        (
            estudiante.id,
            f"{estudiante.carnet} - "
            f"{estudiante.nombres} "
            f"{estudiante.apellidos}"
        )

        for estudiante in
        Estudiante.query.order_by(
            Estudiante.apellidos
        ).all()

    ]

    form.asignatura_id.choices = [

        (
            asignatura.id,
            f"{asignatura.codigo} - "
            f"{asignatura.nombre}"
        )

        for asignatura in
        Asignatura.query.order_by(
            Asignatura.nombre
        ).all()

    ]

    return render_template(
        'inscripciones/lista.html',
        inscripciones=inscripciones,
        form=form
    )


@inscripciones_bp.route(
    '/crear',
    methods=['POST']
)
@login_required
@rol_requerido(
    "Administrador",
    "Docente"
)
def crear():

    form = InscripcionForm()

    form.estudiante_id.choices = [

        (
            estudiante.id,
            estudiante.nombres
        )

        for estudiante in
        Estudiante.query.all()

    ]

    form.asignatura_id.choices = [

        (
            asignatura.id,
            asignatura.nombre
        )

        for asignatura in
        Asignatura.query.all()

    ]

    if form.validate_on_submit():

        existe = Inscripcion.query.filter_by(
            estudiante_id=form.estudiante_id.data,
            asignatura_id=form.asignatura_id.data
        ).first()

        if existe:

            flash(
                'El estudiante ya está inscrito en esta asignatura.',
                'warning'
            )

        else:

            nueva = Inscripcion(
                estudiante_id=form.estudiante_id.data,
                asignatura_id=form.asignatura_id.data
            )

            db.session.add(
                nueva
            )

            db.session.commit()

            flash(
                'Inscripción realizada correctamente.',
                'success'
            )

    return redirect(
        url_for(
            'inscripciones.lista'
        )
    )


@inscripciones_bp.route(
    '/eliminar/<int:id>',
    methods=['POST']
)
@login_required
@rol_requerido(
    "Administrador",
    "Docente"
)
def eliminar(id):

    inscripcion = (
        Inscripcion.query
        .get_or_404(id)
    )

    try:

        db.session.delete(
            inscripcion
        )

        db.session.commit()

        flash(
            'Inscripción eliminada correctamente.',
            'success'
        )

    except Exception:

        db.session.rollback()

        flash(
            'No se pudo eliminar la inscripción.',
            'danger'
        )

    return redirect(
        url_for(
            'inscripciones.lista'
        )
    )


@inscripciones_bp.route(
    '/mis-asignaturas'
)
@login_required
@rol_requerido(
    "Estudiante"
)
def mis_asignaturas():

    estudiante = (
        current_user.estudiante
    )

    inscripciones = (
        Inscripcion.query.filter_by(
            estudiante_id=estudiante.id
        ).all()
    )

    return render_template(
        'inscripciones/mis_asignaturas.html',
        inscripciones=inscripciones
    )