import os
from flask import Flask, request, jsonify, g, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
import logging
from dotenv import load_dotenv
from config import DATABASE_CONFIG

# Carregar o arquivo .env
load_dotenv()

# Obter string de conexão da variável de ambiente
connection_string = os.getenv('DATABASE_URL')

# Inicializa o SQLAlchemy globalmente
db = SQLAlchemy()

# Define o modelo Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

    def json(self):
        return {'id': self.id, 'nome': self.nome, 'email': self.email, 'senha': self.senha}

def create_app():
    app = Flask(__name__)

    # Configura a URI do banco de dados para o SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar avisos

    # Inicializa o SQLAlchemy com a aplicação Flask
    db.init_app(app)

    # Cria as tabelas do banco de dados
    with app.app_context():
        db.create_all()

    # Criar usuário
    @app.route('/usuario', methods=['POST'])
    def create_user():
        try:
            data = request.get_json()
            new_user = Usuario(nome=data['nome'], email=data['email'], senha=data['senha'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'user created'}), 201
        except Exception as e:
            db.session.rollback()  # Reverte a transação em caso de erro
            logging.error(f"Erro ao criar usuário: {e}")
            return jsonify({'message': 'error creating user'}), 500

    # Lista todos os usuários
    @app.route('/usuario', methods=['GET'])
    def get_users():
        try:
            users = Usuario.query.all()
            return jsonify([usuario.json() for usuario in users]), 200
        except Exception as e:
            logging.error(f"Erro ao obter usuários: {e}")
            return jsonify({'message': 'error getting users'}), 500

    # Atualizar
    @app.route("/usuario/<int:id>", methods=["PUT"])
    def update_usuario(id):
        usuario_objeto = Usuario.query.filter_by(id=id).first()
        if usuario_objeto:
            body = request.get_json()
            if body:
                try:
                    if 'nome' in body:
                        usuario_objeto.nome = body['nome']
                    if 'email' in body:
                        usuario_objeto.email = body['email']
                    if 'senha' in body:
                        usuario_objeto.senha = body['senha']

                    db.session.commit()
                    return jsonify({'message': 'usuario updated successfully', 'usuario': usuario_objeto.json()}), 200
                except Exception as e:
                    print('Erro', e)
                    db.session.rollback()
                    return jsonify({'message': 'error updating user'}), 400
            else:
                return jsonify({'message': 'request body is empty'}), 400
        return jsonify({'message': 'user not found'}), 404

    # Deletar
    @app.route("/usuario/<int:id>", methods=["DELETE"])
    def deleta_usuario(id):
        usuario_objeto = Usuario.query.filter_by(id=id).first()
        if usuario_objeto:
            try:
                db.session.delete(usuario_objeto)
                db.session.commit()
                return jsonify({'message': 'usuario deleted successfully'}), 200
            except Exception as e:
                print('Erro', e)
                db.session.rollback()  # Em caso de erro, desfaz as alterações na sessão
                return jsonify({'message': 'error deleting user'}), 400
        return jsonify({'message': 'user not found'}), 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)