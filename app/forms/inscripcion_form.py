from flask_wtf import FlaskForm

from wtforms import SelectField
from wtforms import SubmitField

from wtforms.validators import DataRequired


class InscripcionForm(FlaskForm):

    estudiante_id = SelectField(
        'Estudiante',
        validators=[
            DataRequired()
        ],
        coerce=int
    )

    asignatura_id = SelectField(
        'Asignatura',
        validators=[
            DataRequired()
        ],
        coerce=int
    )

    submit = SubmitField(
        'Guardar Inscripción'
    )