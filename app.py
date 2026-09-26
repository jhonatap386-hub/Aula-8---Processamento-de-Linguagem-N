from flask import Flask
from controllers.routes import routes_bp
from models.intent_model import init_db

app = Flask(__name__)

# Inicializa banco de dados
init_db()

# Registra as rotas (MVC)
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)