from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class AsignaturaForm(FlaskForm):
    codigo = StringField('Código de la Asignatura', validators=[
        DataRequired(message="El código es obligatorio."),
        Length(min=3, max=20, message="El código debe tener entre 3 y 20 caracteres.")
    ])
    nombre = StringField('Nombre de la Asignatura', validators=[
        DataRequired(message="El nombre de la materia es obligatorio."),
        Length(max=100)
    ])
    descripcion = TextAreaField('Descripción (Opcional)', validators=[
        Length(max=255, message="La descripción no puede pasar de 255 caracteres.")
    ])
    submit = SubmitField('Guardar Asignatura')