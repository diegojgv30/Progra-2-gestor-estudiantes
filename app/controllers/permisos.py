from functools import wraps

from flask import flash
from flask import redirect
from flask import url_for

from flask_login import current_user


def rol_requerido(*roles_permitidos):

    def decorador(func):

        @wraps(func)
        def envoltura(*args, **kwargs):

            if not current_user.is_authenticated:

                flash(
                    "Debes iniciar sesión para acceder.",
                    "warning"
                )

                return redirect(
                    url_for("auth.login")
                )

            if current_user.rol.nombre not in roles_permitidos:

                flash(
                    "No tienes permisos para acceder a esta sección.",
                    "danger"
                )

                return redirect(
                    url_for("auth.dashboard")
                )

            return func(*args, **kwargs)

        return envoltura

    return decorador