# Criar estrutura do banco de dados
from datetime import datetime
from flask import flash
from flask_login import UserMixin # Define qual a Classe que gerencia o login
from FlaskRifas import database, login_manager


# Carregar Úsuario
@login_manager.user_loader
def load_usuario(id_usuario):
    try:
        return Usuario.query.get(id_usuario)
    except:
        flash('Usuário já existe')

# Criar úsuarios
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, unique=True, nullable=False)
    email = database.Column(database.String, unique=True, nullable=False)
    telefone = database.Column(database.String, unique=True, nullable=False)
    equipe = database.Column(database.String, default='Cliente')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    cotas = database.relationship('Numero', backref='usuario', lazy=True)
    pagamentos = database.relationship('Pagamento', backref='usuario', lazy=True)
    rifas = database.relationship('Rifa', backref='usuario', lazy=True)
    # credenciais = database.relationship('Credenciais', backref='usuario', lazy=True)

# Criar rifas
class Rifa(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.String, nullable=False)
    qnty_cotas = database.Column(database.Integer, nullable = False)
    valor = database.Column(database.String, nullable=False)
    sorteio = database.Column(database.String, nullable=False, default='A Definir')
    status = database.Column(database.String, nullable=False, default='Em Andamento')
    ganhador = database.Column(database.String, nullable=False, default='A Definir')
    imagem = database.Column(database.String, default='rifas/padrão.jpg')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    criador = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    cotas = database.relationship('Numero', backref='rifa', lazy=True)
    pagamentos = database.relationship('Pagamento', backref='rifa', lazy=True)

# Criar cotas
class Numero(database.Model):
    id = database.Column(database.Integer, primary_key=True) 
    id_rifa = database.Column(database.Integer, database.ForeignKey('rifa.id'), nullable=False) 
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), default='') 
    id_pagamento = database.Column(database.Integer, database.ForeignKey('pagamento.txid'), default='') 
    cota = database.Column(database.Integer, nullable=False) 
    valor = database.Column(database.String, nullable=False)
    status = database.Column(database.String, default='Disponível')
    data_compra = database.Column(database.DateTime, nullable=True)

# Armazenar pagamentos
class Pagamento(database.Model):
    id = database.Column(database.Integer, primary_key=True) 
    txid = database.Column(database.String, unique=True, nullable=False)
    endid = database.Column(database.String, nullable=True)
    id_rifa = database.Column(database.Integer, database.ForeignKey('rifa.id'), nullable=False) 
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False) 
    valor = database.Column(database.String, nullable=False)
    qnty_cotas = database.Column(database.Integer, nullable=False)
    cotas = database.Column(database.String, nullable=False)
    status = database.Column(database.String, default='Não concluído')
    qrcode = database.Column(database.String, nullable=True)
    data_pagamento = database.Column(database.DateTime, nullable=False)

# Suporte
class Suporte(database.Model):
    id = database.Column(database.Integer, primary_key=True) 
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    descricao = database.Column(database.String, nullable=False)
    status = database.Column(database.String, nullable=False)
    solucao = database.Column(database.String, nullable=True)
    data_criacao = database.Column(database.DateTime, default=datetime.now())


# relacionamento
# definir relacionamento apenas para quem exporta a ForeignKey.
# nome = database.relationship('nome_tabela', backref='nome_tabela' lazy=True)
# id_nome = database.Column(database.Integer, database.ForeignKey('nome_tabela.coluna_id'), nullable=False)