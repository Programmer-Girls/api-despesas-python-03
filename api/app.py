from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from dotenv import load_dotenv
from config import SQLALCHEMY_DATABASE_URI
from extensions import db, jwt
from blueprints.usuario.usuario import usuario_bp
from blueprints.despesa.despesa import despesa_bp
from blueprints.categoria.categoria import categoria_bp, categorias_padrao
import os  # Import os module

# Carregar o arquivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configura a URI do banco de dados para o SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar avisos

    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'super-secret') # Configure a chave secreta JWT


    # Inicializa o SQLAlchemy e o JWT com a aplicação Flask
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        categorias_padrao()


    app.register_blueprint(despesa_bp, url_prefix='/despesa')
    app.register_blueprint(categoria_bp, url_prefix='/categoria')
    app.register_blueprint(usuario_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)