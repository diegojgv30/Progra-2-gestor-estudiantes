from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class EstudianteForm(FlaskForm):
    carnet = StringField('Carnet', validators=[
        DataRequired(message="El carnet es obligatorio."),
        Length(min=3, max=20, message="El carnet debe tener entre 3 y 20 caracteres.")
    ])
    nombres = StringField('Nombres', validators=[
        DataRequired(message="Los nombres son obligatorios."),
        Length(max=100)
    ])
    apellidos = StringField('Apellidos', validators=[
        DataRequired(message="Los apellidos son obligatorios."),
        Length(max=100)
    ])
    correo = StringField('Correo Electrónico', validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Ingresa un correo electrónico válido."),
        Length(max=120)
    ])
    submit = SubmitField('Guardar Estudiante')