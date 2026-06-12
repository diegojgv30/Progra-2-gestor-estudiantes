from app import create_app

# Creamos la aplicación usando nuestra fábrica limpia
app = create_app()

# Busca la línea final y déjala así:
if __name__ == '__main__':
    app.run(debug=True, port=5001)