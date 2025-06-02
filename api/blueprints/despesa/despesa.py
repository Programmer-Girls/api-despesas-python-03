from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Despesa

despesa_bp = Blueprint('despesa', __name__)


@despesa_bp.route('/novadespesa', methods=['POST'])
@jwt_required()
def criardespesa():
    try:
        id_usuario = int(get_jwt_identity())

        nova_despesa = request.get_json()

        if not nova_despesa:
            return jsonify({'msg': 'Dados Insuficientes'}), 400

        despesa = Despesa(
            descricao = nova_despesa['descricao'],
            valor = nova_despesa['valor'],
            id_categoria = nova_despesa['id_categoria'],
            id_usuario = id_usuario
            )
        
        # Adiciona a nova despesa ao banco
        db.session.add(despesa)
        db.session.commit()
        db.session.refresh(despesa)
    
        return jsonify({'msg': 'Despesa Cadastrada Com Sucesso!'}, despesa.json()),201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar despesa: {str(e)}")
        return jsonify(msg='Erro ao cadastrar despesa'), 500

# <int:id> para tornar dinâmico, se colocar apenas /id ele entende como str
@despesa_bp.route('/atualizar/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar(id):
   try:
    id_usuario = int(get_jwt_identity())

    despesa_atualizar = Despesa.query.filter_by(id=id, id_usuario=id_usuario).first()

    if not despesa_atualizar:
        return jsonify(msg='Despesa Não Encontrada!'), 404
    
    dados = request.get_json()
    if 'descricao' in dados:
        despesa_atualizar.descricao = dados['descricao']
    if 'valor' in dados:
        despesa_atualizar.valor = dados['valor']
    if 'id_categoria' in dados:
        despesa_atualizar.id_categoria = dados['id_categoria']
    
    db.session.commit()

    return jsonify({'msg': 'Despesa Atualizada Com Sucesso!'}, despesa_atualizar.json()), 200
   except Exception as e:
       db.session.rollback()
       print(f"Erro ao atualizar despesa: {str(e)}")
       return jsonify(msg='Erro ao atualizar despesa'), 500

@despesa_bp.route('/')
@jwt_required()
def listar():
    try:
        # Identificar usuário logado
        id_usuario = int(get_jwt_identity())

        # Filtrar apenas as despesas do usuário logado
        query = Despesa.query.filter_by(id_usuario=id_usuario) # retorna uma lista de objetos

        valor_min = request.args.get('valor_min')
        valor_max = request.args.get('valor_max')
        categoria = request.args.get('id_categoria')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')

        # Checar e aplicar os filtros na listagem
        if valor_min is not None:
            try:
                query = query.filter(Despesa.valor >= valor_min)
            except ValueError:
                return jsonify({'msg': 'Valor Inválido'}), 400
        
        
        if valor_max is not None:
            try:
                query = query.filter(Despesa.valor <= valor_max)
            except ValueError:
                return jsonify({'msg': 'Valor Inválido'}), 400
            

        if categoria is not None:
            try:
                query = query.filter_by(id_categoria=int(categoria))
            except ValueError:
                return jsonify({'msg': 'Categoria Inválida'}), 400
        
        
        if data_inicio is not None:
            try:
                from datetime import date
                data_obj = date.fromisoformat(data_inicio)
                query = query.filter(Despesa.data >= data_obj)
            except ValueError:
                return jsonify({'msg': 'Data Inválida'}), 400
            
        if data_fim is not None:
            try:
                from datetime import date
                data_obj = date.fromisoformat(data_fim)
                query = query.filter(Despesa.data <= data_obj)
            except ValueError:
                return jsonify({'msg': 'Data Inválida'}), 400

        despesas = query.all()
        if not despesas:
            return jsonify({'msg': 'Vazio!'}), 200

        return jsonify([despesa.json() for despesa in despesas]), 200
    except Exception as e:
        print(f"Erro ao listar despesas: {str(e)}")
        return jsonify(msg='Erro ao listar despesas'), 500
    

@despesa_bp.route('/deletar/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar(id):
    try:
        
        id_usuario = int(get_jwt_identity())

        despesa_deletar = Despesa.query.filter_by(id=id, id_usuario=id_usuario).first()

        if not despesa_deletar:
            return jsonify(msg='Despesa Não Encontrada'), 404
        
        db.session.delete(despesa_deletar)
        db.session.commit()

        return jsonify(msg='Despesa deletada com sucesso'), 200
    except Exception as e:
       db.session.rollback()
       print(f"Erro ao deletar despesa: {str(e)}")
       return jsonify(msg='Erro ao deletar despesa'), 500