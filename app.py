from flask import Flask
from routes.user_routes import user_bp
from routes.service_routes import service_bp

app = Flask(__name__)

# Registra o Blueprint das rotas de usuário
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(service_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
