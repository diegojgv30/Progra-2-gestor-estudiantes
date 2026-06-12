from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import login_required
from flask_login import current_user

from config.database import db

from app.models.calificacion import Calificacion
from app.models.inscripcion import Inscripcion
from app.models.estudiante import Estudiante

from app.forms.calificacion_form import CalificacionForm

from app.controllers.permisos import rol_requerido


calificaciones_bp = Blueprint(
    'calificaciones',
    __name__,
    url_prefix='/calificaciones'
)


@calificaciones_bp.route('/')
@login_required
@rol_requerido(
    "Administrador",
    "Docente"
)
def lista():

    busqueda = request.args.get(
        'buscar',
        ''
    ).strip()

    calificaciones_query = (
        Calificacion.query
        .join(Inscripcion)
        .join(Estudiante)
    )

    if busqueda:

        calificaciones_query = (
            calificaciones_query.filter(
                db.or_(
                    Estudiante.nombres.ilike(
                        f'%{busqueda}%'
                    ),
                    Estudiante.apellidos.ilike(
                        f'%{busqueda}%'
                    ),
                    Estudiante.carnet.ilike(
                        f'%{busqueda}%'
                    ),
                    Calificacion.nota.cast(
                        db.String
                    ).ilike(
                        f'%{busqueda}%'
                    )
                )
            )
        )

    calificaciones = (
        calificaciones_query
        .all()
    )

    return render_template(
        'calificaciones/lista.html',
        calificaciones=calificaciones,
        busqueda=busqueda
    )


@calificaciones_bp.route(
    '/nuevo',
    methods=['GET', 'POST']
)
@login_required
@rol_requerido(
    "Administrador",
    "Docente"
)
def nuevo():

    form = CalificacionForm()

    inscripciones = (
        Inscripcion.query
        .all()
    )

    form.inscripcion_id.choices = [

        (
            i.id,
            (
                f"{i.estudiante.carnet} - "
                f"{i.estudiante.nombres} "
                f"{i.estudiante.apellidos} - "
                f"{i.asignatura.nombre}"
            )
        )

        for i in inscripciones

    ]

    if form.validate_on_submit():

        existe = Calificacion.query.filter_by(
            inscripcion_id=form.inscripcion_id.data
        ).first()

        if existe:

            flash(
                'Esta inscripción ya posee una calificación.',
                'warning'
            )

            return render_template(
                'calificaciones/editar.html',
                form=form
            )

        nueva_calificacion = Calificacion(
            inscripcion_id=form.inscripcion_id.data,
            nota=form.nota.data
        )

        db.session.add(
            nueva_calificacion
        )

        db.session.commit()

        flash(
            'Calificación registrada correctamente.',
            'success'
        )

        return redirect(
            url_for(
                'calificaciones.lista'
            )
        )

    return render_template(
        'calificaciones/editar.html',
        form=form
    )


@calificaciones_bp.route(
    '/editar/<int:id>',
    methods=['GET', 'POST']
)
@login_required
@rol_requerido(
    "Administrador",
    "Docente"
)
def editar(id):

    calificacion = (
        Calificacion.query
        .get_or_404(id)
    )

    form = CalificacionForm(
        obj=calificacion
    )

    inscripciones = (
        Inscripcion.query
        .all()
    )

    form.inscripcion_id.choices = [

        (
            i.id,
            (
                f"{i.estudiante.carnet} - "
                f"{i.estudiante.nombres} "
                f"{i.estudiante.apellidos} - "
                f"{i.asignatura.nombre}"
            )
        )

        for i in inscripciones

    ]

    if form.validate_on_submit():

        existe = (
            Calificacion.query.filter(
                Calificacion.inscripcion_id ==
                form.inscripcion_id.data,

                Calificacion.id != id
            ).first()
        )

        if existe:

            flash(
                'La inscripción seleccionada ya tiene una calificación.',
                'warning'
            )

            return render_template(
                'calificaciones/editar.html',
                form=form
            )

        calificacion.inscripcion_id = (
            form.inscripcion_id.data
        )

        calificacion.nota = (
            form.nota.data
        )

        db.session.commit()

        flash(
            'Calificación actualizada.',
            'success'
        )

        return redirect(
            url_for(
                'calificaciones.lista'
            )
        )

    return render_template(
        'calificaciones/editar.html',
        form=form
    )


@calificaciones_bp.route(
    '/eliminar/<int:id>',
    methods=['POST']
)
@login_required
@rol_requerido(
    "Administrador",
    "Docente"
)
def eliminar(id):

    calificacion = (
        Calificacion.query
        .get_or_404(id)
    )

    db.session.delete(
        calificacion
    )

    db.session.commit()

    flash(
        'Calificación eliminada.',
        'success'
    )

    return redirect(
        url_for(
            'calificaciones.lista'
        )
    )


@calificaciones_bp.route(
    '/mis-calificaciones'
)
@login_required
@rol_requerido(
    "Estudiante"
)
def mis_calificaciones():

    estudiante = (
        current_user.estudiante
    )

    calificaciones = (

        Calificacion.query

        .join(Inscripcion)

        .filter(
            Inscripcion.estudiante_id ==
            estudiante.id
        )

        .all()

    )

    return render_template(
        'calificaciones/mis_calificaciones.html',
        calificaciones=calificaciones
    )