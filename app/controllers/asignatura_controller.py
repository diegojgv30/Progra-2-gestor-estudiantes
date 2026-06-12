from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import login_required

from config.database import db

from app.models.asignatura import Asignatura

from app.forms.asignatura_form import AsignaturaForm

from app.controllers.permisos import rol_requerido


asignaturas_bp = Blueprint(
    'asignaturas',
    __name__,
    url_prefix='/asignaturas'
)


@asignaturas_bp.route('/')
@login_required
@rol_requerido(
    "Administrador",
    "Docente"
)
def lista():

    form = AsignaturaForm()

    busqueda = request.args.get(
        'buscar',
        ''
    ).strip()

    asignaturas_query = Asignatura.query

    if busqueda:

        asignaturas_query = asignaturas_query.filter(
            db.or_(
                Asignatura.codigo.ilike(
                    f'%{busqueda}%'
                ),
                Asignatura.nombre.ilike(
                    f'%{busqueda}%'
                ),
                Asignatura.descripcion.ilike(
                    f'%{busqueda}%'
                )
            )
        )

    asignaturas = asignaturas_query.order_by(
        Asignatura.nombre.asc()
    ).all()

    return render_template(
        'asignaturas/lista.html',
        asignaturas=asignaturas,
        form=form,
        busqueda=busqueda
    )


@asignaturas_bp.route(
    '/crear',
    methods=['POST']
)
@login_required
@rol_requerido(
    "Administrador"
)
def crear():

    form = AsignaturaForm()

    if form.validate_on_submit():

        existe_codigo = Asignatura.query.filter_by(
            codigo=form.codigo.data.upper()
        ).first()

        if existe_codigo:

            flash(
                'El código de asignatura ya existe en el sistema.',
                'danger'
            )

            return redirect(
                url_for('asignaturas.lista')
            )

        nueva_materia = Asignatura(
            codigo=form.codigo.data.upper(),
            nombre=form.nombre.data,
            descripcion=form.descripcion.data
        )

        db.session.add(
            nueva_materia
        )

        db.session.commit()

        flash(
            'Asignatura creada correctamente.',
            'success'
        )

    else:

        for field, errors in form.errors.items():

            for error in errors:

                flash(
                    f"Error: {error}",
                    'danger'
                )

    return redirect(
        url_for('asignaturas.lista')
    )


@asignaturas_bp.route(
    '/eliminar/<int:id>',
    methods=['POST']
)
@login_required
@rol_requerido(
    "Administrador"
)
def eliminar(id):

    asignatura = Asignatura.query.get_or_404(
        id
    )

    try:

        db.session.delete(
            asignatura
        )

        db.session.commit()

        flash(
            'Asignatura eliminada exitosamente.',
            'success'
        )

    except Exception:

        db.session.rollback()

        flash(
            'No se puede eliminar la materia porque tiene estudiantes inscritos.',
            'danger'
        )

    return redirect(
        url_for('asignaturas.lista')
    )


@asignaturas_bp.route(
    '/editar/<int:id>',
    methods=['GET', 'POST']
)
@login_required
@rol_requerido(
    "Administrador"
)
def editar(id):

    asignatura = Asignatura.query.get_or_404(
        id
    )

    form = AsignaturaForm(
        obj=asignatura
    )

    if form.validate_on_submit():

        choque_codigo = Asignatura.query.filter(
            Asignatura.codigo == form.codigo.data.upper(),
            Asignatura.id != id
        ).first()

        if choque_codigo:

            flash(
                'El código de asignatura ya pertenece a otra materia.',
                'danger'
            )

            return render_template(
                'asignaturas/editar.html',
                form=form,
                asignatura=asignatura
            )

        asignatura.codigo = (
            form.codigo.data.upper()
        )

        asignatura.nombre = (
            form.nombre.data
        )

        asignatura.descripcion = (
            form.descripcion.data
        )

        db.session.commit()

        flash(
            'Asignatura actualizada exitosamente.',
            'success'
        )

        return redirect(
            url_for('asignaturas.lista')
        )

    return render_template(
        'asignaturas/editar.html',
        form=form,
        asignatura=asignatura
    )