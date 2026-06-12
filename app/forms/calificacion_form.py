from flask_wtf import FlaskForm

from wtforms import (
    FloatField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    NumberRange
)


class CalificacionForm(FlaskForm):

    inscripcion_id = SelectField(
        'Estudiante / Asignatura',
        validators=[
            DataRequired()
        ],
        coerce=int
    )

    nota = FloatField(
        'Nota',
        validators=[
            DataRequired(),
            NumberRange(
                min=0.00,
                max=10.00,
                message=(
                    'La nota debe estar entre '
                    '0.00 y 10.00.'
                )
            )
        ]
    )

    submit = SubmitField(
        'Guardar Calificación'
    )