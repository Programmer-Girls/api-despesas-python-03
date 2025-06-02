from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Categoria

categoria_bp = Blueprint('categoria', __name__)

# Define as categorias pré-definidas do sistema
def categorias_padrao():
    categorias_padrao = ['Alimentação', 'Lazer', 'Transporte', 'Saúde', 'Educação']
    for nome in categorias_padrao:
        existente = Categoria.query.filter_by(nome=nome, id_usuario=None).first()
        if not existente:
            nova = Categoria(nome=nome)
            db.session.add(nova)
    db.session.commit()

@categoria_bp.route('/novacategoria', methods=['POST'])
@jwt_required()
def criar():
    try:
        id_usuario = int(get_jwt_identity())

        nova_categoria = request.get_json()

        if not nova_categoria:
            return jsonify({'msg': 'Despesa não criada por falta de dados'}), 400
        
        categoria = Categoria(
            nome = nova_categoria['nome'],
            id_usuario = id_usuario
        )
        db.session.add(categoria)
        db.session.commit()
        db.session.refresh(categoria)

        return jsonify({'msg': 'Nova Categoria Criada Com Sucesso!'}, categoria.json()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar nova categoria: {str(e)}")
        return jsonify(msg='Erro ao cadastrar despesa'), 500 

@categoria_bp.route('/deletar/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar(id):
    try:
        id_usuario = int(get_jwt_identity())
        categoria_deletar = Categoria.query.filter_by(id=id, id_usuario=id_usuario).first()

        if not categoria_deletar:
            return jsonify({'msg': 'Categoria não encontrada'}), 404
        
        db.session.delete(categoria_deletar)
        db.session.commit()
        return jsonify({'msg': 'Categoria deletada com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar categoria: {str(e)}")
        return jsonify(msg='Erro ao deletar categoria'), 500
    
@categoria_bp.route('/atualizar/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar(id):
    try:
        id_usuario = int(get_jwt_identity())

        categoria_atualizar = Categoria.query.filter_by(id=id, id_usuario=id_usuario).first()

        if not categoria_atualizar:
            return jsonify({'msg': 'Categoria não encontrada'}), 404
        
        nome = request.get_json()
        categoria_atualizar.nome = nome['nome']

        db.session.commit()
        return jsonify({'msg':'Categoria atualizadoa com sucesso'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar categoria: {str(e)}")
        return jsonify(msg='Erro ao atualizar categoria'), 500

@categoria_bp.route('/')
@jwt_required()
def listar():
    try:
        id_usuario = int(get_jwt_identity())
        categorias = Categoria.query.filter((Categoria.id_usuario == id_usuario) | (Categoria.id_usuario == None)).all()
        return jsonify([categoria.json() for categoria in categorias]), 200
    except Exception as e:
        print(f"Erro ao listar categorias: {str(e)}")
        return jsonify(msg='Erro ao listar categorias'), 500