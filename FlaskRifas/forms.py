from flask_wtf import FlaskForm
from wtforms import DateField, StringField, TelField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length

# Form de login
class FormLogin(FlaskForm):
    telefone = StringField('Telefone', validators=[DataRequired(), Length(11,11)])
    lembrar = BooleanField('Lembrar')
    botao = SubmitField('Login')

# Form criar conta
class FormCriarConta(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(11,11)])
    botao = SubmitField('Criar Conta')

# Form Alterar Rifas
class FormEditarRifas(FlaskForm):
    qnty_cotas = IntegerField('Quantidade Bilhete:')
    cota_premiada = SubmitField('Gerar')
    sorteio = DateField('Sorteio:')
    descricao = StringField('Descrição:')
    alterar = SubmitField('Alterar')

# Form Suporte
class FormSuporte(FlaskForm):
    descricao = StringField('Descrição:')
    enviar = SubmitField('Enviar')
    solucao = StringField('Solução:')
    resolver = SubmitField('Resolver')