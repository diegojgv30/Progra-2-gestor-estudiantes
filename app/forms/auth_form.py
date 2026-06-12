from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    correo = StringField('Correo Institucional', validators=[
        DataRequired(message="El correo electrónico es obligatorio."),
        Email(message="Por favor, ingresa un correo electrónico válido.")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria.")
    ])
    recordarme = BooleanField('Mantener sesión iniciada')
    submit = SubmitField('Iniciar Sesión')