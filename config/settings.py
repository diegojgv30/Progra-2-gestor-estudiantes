import os


class Config:

    SECRET_KEY = (
        os.environ.get('SECRET_KEY')
        or
        'clave_secreta_super_segura_12345'
    )

    BASE_DIR = os.path.abspath(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )

    INSTANCE_DIR = os.path.join(
        BASE_DIR,
        'instance'
    )

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(INSTANCE_DIR, 'sistema_estudiantil.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False