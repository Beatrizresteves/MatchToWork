from flask import Flask
from routes.user_routes import user_bp
from routes.service_routes import service_bp
from routes.service_type_routes import service_type_bp

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(service_bp, url_prefix='/api')
app.register_blueprint(service_type_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
