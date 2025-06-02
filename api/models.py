from extensions import db 
from datetime import date

# TABELAS DO BANCO

# Modelo Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

    def json(self):
        return {'id': self.id, 'nome': self.nome, 'email': self.email, 'senha': self.senha}
    
#Modelo Categoria
class Categoria(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     nome = db.Column(db.String(80), nullable=False)
     id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id), nullable=True)

     # Relacionamento
     usuario = db.relationship('Usuario', backref='categorias', lazy=True)

     def json(self):
          return {
               'id': self.id,
               'nome': self.nome,
               'usuario': 'Sistema' if self.usuario is None else self.usuario.nome}
    
# Modelo Despesa
class Despesa(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        descricao = db.Column(db.String(100), nullable=False)
        valor = db.Column(db.Float, nullable=False)
        data = db.Column(db.Date, default=date.today)
        id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id))
        id_categoria = db.Column(db.Integer, db.ForeignKey(Categoria.id))

        # Relacionamentos
        usuario = db.relationship('Usuario', backref='despesas', lazy=True)
        categoria = db.relationship('Categoria', backref='despesas', lazy=True)

        def json(self):
             return {
                  'id': self.id, 
                  'descricao': self.descricao, 
                  'valor': self.valor,
                  'data': self.data.isoformat(),
                  'usuario': self.usuario.nome if self.usuario else None,
                  'categoria': self.categoria.nome if self.categoria else None}
