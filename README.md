# Sistema de Gestión Académica - Universidad de El Salvador

Sistema web desarrollado con Flask para la gestión académica universitaria, permitiendo administrar estudiantes, asignaturas, inscripciones y calificaciones mediante diferentes roles de usuario.

---

## Características

- Inicio de sesión con autenticación de usuarios.
- Gestión de estudiantes.
- Gestión de asignaturas.
- Gestión de inscripciones.
- Gestión de calificaciones.
- Dashboard personalizado según el rol del usuario.
- Roles del sistema:
  - Administrador
  - Docente
  - Estudiante
- Base de datos SQLite.
- Interfaz responsive utilizando Bootstrap 5.

---

## Tecnologías utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- WTForms
- SQLite
- Bootstrap 5
- HTML5
- CSS3
- Jinja2

---

## Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

### Python

Verificar instalación:

```bash
python --version
```

o

```bash
py --version
```

Debe mostrar una versión igual o superior a:

```text
Python 3.10
```

Si no está instalado, descargar desde:

https://www.python.org/downloads/

**Importante:** Durante la instalación marcar la opción:

```text
✓ Add Python to PATH
```

---

## Obtener el proyecto

### Opción 1: Clonar desde GitHub

```bash
git clone https://github.com/diegojgv30/analisis-de-sistemas-2-gestor-estudiantes.git
```

Ingresar a la carpeta del proyecto:

```bash
cd analisis-de-sistemas-2-gestor-estudiantes
```

---

### Opción 2: Descargar ZIP

1. Abrir el repositorio en GitHub.
2. Presionar el botón **Code**.
3. Seleccionar **Download ZIP**.
4. Extraer el contenido.
5. Abrir una terminal dentro de la carpeta del proyecto.

---

## Crear entorno virtual

### Windows

```bash
python -m venv venv
```

o

```bash
py -m venv venv
```

### Linux / WSL

```bash
python3 -m venv venv
```

---

## Activar entorno virtual

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

Si aparece un error relacionado con políticas de ejecución, ejecutar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego volver a ejecutar:

```powershell
.\venv\Scripts\Activate.ps1
```

---

### Windows CMD

```cmd
venv\Scripts\activate.bat
```

---

### Linux / WSL

```bash
source venv/bin/activate
```

Cuando el entorno virtual esté activo aparecerá algo similar a:

```text
(venv)
```

al inicio de la terminal.

---

## Instalar dependencias

Con el entorno virtual activado ejecutar:

```bash
pip install -r requirements.txt
```

Este comando instalará automáticamente todas las librerías necesarias para ejecutar el proyecto.

---

## Base de datos

El proyecto utiliza **SQLite**.

La base de datos ya está incluida en el repositorio:

```text
instance/sistema_estudiantil.db
```

Por lo tanto, **NO es necesario crear bases de datos ni ejecutar scripts SQL adicionales**.

---

## Ejecutar la aplicación

Con el entorno virtual activado ejecutar:

```bash
python run.py
```

o:

```bash
python app.py
```

según el archivo principal del proyecto.

---

## Acceder al sistema

Una vez iniciado el servidor aparecerá un mensaje similar a:

```text
Running on http://127.0.0.1:5000
```

Abrir el navegador y acceder a:

```text
http://127.0.0.1:5000
```

---

## Estructura del proyecto

```text
analisis-de-sistemas-2-gestor-estudiantes/
│
├── app/
│   ├── controllers/
│   ├── forms/
│   ├── models/
│   ├── templates/
│   └── static/
│
├── config/
│
├── instance/
│   └── sistema_estudiantil.db
│
├── migrations/            (si aplica)
│
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

---

## Solución de problemas comunes

### Error: Python no reconocido

Instalar Python y asegurarse de marcar:

```text
✓ Add Python to PATH
```

---

### Error: pip no reconocido

Ejecutar:

```bash
python -m pip install --upgrade pip
```

---

### Error: No module named 'xxxx'

Verificar que:

1. El entorno virtual esté activado.
2. Se haya ejecutado:

```bash
pip install -r requirements.txt
```

---

### Error al activar el entorno virtual en PowerShell

Ejecutar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Error: Address already in use

El puerto 5000 está siendo utilizado por otra aplicación.

Detener la aplicación que utiliza el puerto o modificar el puerto de ejecución en el proyecto.

---

## Credenciales de acceso

Utilizar las credenciales proporcionadas por el desarrollador o las cuentas incluidas en la base de datos SQLite.

---

## Autor

Desarrollado como proyecto académico para la asignatura:

**Análisis de Sistemas II**

Universidad de El Salvador.
