from flask import Flask
from api.routes import user_bp

app = Flask(__name__)

# Registra o Blueprint das rotas de usuário
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
