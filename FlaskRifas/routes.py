import os
 
from sqlalchemy import desc
from FlaskRifas.forms import *
from FlaskRifas.models import *
from FlaskRifas.funcoes import *
from FlaskRifas.api import PixModel
from FlaskRifas import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from FlaskRifas import app, database, bcrypt
from werkzeug.utils import secure_filename 
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, url_for, request, redirect, flash, Response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Definir Rotas
@app.route('/')
def homepage():
    users = Usuario.query.all()
    numeros = Numero.query.all()
    rifas = Rifa.query.all()
    pagamentos = Pagamento.query.all()

    try:
        reservados('Reservado')
        reservados('Pago')
    except:
        pass
    # Retornar o números reservados para Disponível
    
    return render_template('Homepage.html', pag='homepage', users=users, numeros=numeros, rifas=rifas, pagamentos=pagamentos)

# Carregar
@app.route('/carregar')
def carregar():
    users = Usuario.query.all()
    numeros = Numero.query.all()
    rifas = Rifa.query.all()
    pagamentos = Pagamento.query.all()
    return render_template('Carregar.html', pag='carregar', users=users, numeros=numeros, rifas=rifas, pagamentos=pagamentos)

# Criar Conta
@app.route('/criarconta/<valor>/<titulo>/<int:cotas>/<int:id_rifa>', methods=['GET', 'POST'])
def criarconta(valor, titulo, cotas, id_rifa):
    # Formulário da página
    form = FormCriarConta() 
  
    # Verificar formulário
    if request.method == 'POST':
        # Pegar Dados HTMl
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        # Criar o usuário
        try:
            usuario = Usuario(
                nome = nome,
                email = email,
                telefone = telefone,
            )

            # Salvar e commitar
            database.session.add(usuario)
            database.session.commit()
            
            # Logar
            login_user(usuario)
            # Redirecionar para a tela de login
            return redirect(url_for('login', valor=valor, titulo=titulo, cotas=cotas, id_rifa=id_rifa))
        except:
            pass

    return render_template('Criarconta.html', form=form, valor=valor, titulo=titulo, cotas=cotas, id_rifa=id_rifa, pag='criarconta')

@app.route('/criarconta2', methods=['GET','POST'])
def criarconta2():
    # Formulário da página
    form = FormCriarConta() 
    try:
        # Verificar formulário
        if request.method == 'POST':
            # Pegar Dados HTMl
            nome = request.form['nome']
            email = request.form['email']
            telefone = request.form['telefone']

            # Criar o usuário
            
            usuario = Usuario(
                nome = nome,
                email = email,
                telefone = telefone,
            )

            # Salvar e commitar
            database.session.add(usuario)
            database.session.commit()
            
            # Logar
            login_user(usuario)
            # Redirecionar para a tela de login
            return redirect(url_for('login2'))
    except:
        pass    
    return render_template('Criarconta.html', form=form, pag='criarconta2')

# Login
@app.route('/login/<valor>/<titulo>/<int:cotas>/<int:id_rifa>', methods=['GET', 'POST'])
def login(valor, titulo, cotas, id_rifa):
    form = FormLogin() 

    if request.method == 'POST':
        # Pegar dados HTML
        telefone = request.form['telefone']
        
        # Filtrar usuário
        usuario = Usuario.query.filter_by(telefone=telefone).first()
        # Verificar se o usuário existe
        if usuario:
            # Logar usuário
            login_user(usuario)
            # Redirecionar o usuário logado
            return redirect(url_for('login', valor=valor, titulo=titulo, cotas=cotas, id_rifa=id_rifa))
        else:
            flash('Login Inválido, Tente Novamente!')
            # Redirecionar para criar conta
            return redirect(url_for('criarconta', valor=valor, titulo=titulo, cotas=cotas, id_rifa=id_rifa))
    # Liberar números reservados não pagos no prazo
    try:
        reservados('Reservado')
        reservados('Pago')
    except:
        pass
    return render_template('Login.html', form=form, valor=valor, titulo=titulo, cotas=cotas, id_rifa=id_rifa, pag='login')

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    form = FormLogin() 
    
    # Verificar se há algum usuário logado
    if current_user == '':
        pass
    else:
        logout_user()

    if request.method == 'POST':
        # Pegar dados HTML
        telefone = request.form['telefone']
        
        # Filtrar usuário
        usuario = Usuario.query.filter_by(telefone=telefone).first()
        # Verificar se o usuário existe
        if usuario:
            # Logar usuário
            login_user(usuario)
            # Redirecionar o usuário logado
            # return redirect(url_for('login2'))
        else:
            flash('Login Inválido, Tente Novamente!')
            # Redirecionar para criar conta
            return redirect(url_for('criarconta2'))
    # Liberar números reservados não pagos no prazo
    try:
        reservados('Reservado')
        reservados('Pago')
    except:
        pass
    return render_template('Login.html', form=form, pag='login2')


# Sair
@app.route('/logout/<valor>/<titulo>/<int:cotas>/<int:id_rifa>', methods=['GET', 'POST'])
def logout(valor, titulo, cotas, id_rifa):
    logout_user() 
    return redirect(url_for('login', valor=valor, titulo=titulo, cotas=cotas, id_rifa=id_rifa))

# Loja 
@app.route('/loja')
def loja():
    # Filtrar Rifas, ordenalas pelo id
    bd_rifas = Rifa.query.order_by(desc(column='id')).all()

    # Verificar status das rifas
    for i in bd_rifas:
        statusRifas(i.id)

    # Retornar o números reservados para Disponível
    
    try:
        reservados('Reservado')
        reservados('Pago')
    except:
        pass

    return render_template('Loja.html', rifas = bd_rifas) 

# Criar Rifas ADM 
@app.route('/criarrifas/686b99561e<int:id>d8d3a6cb63d70adca6d46c9ac9e808b3847fa4', methods=['GET', 'POST'])
@login_required
def criarrifas(id):
    # Banco de Dados
    rifas = Rifa.query.order_by(desc(column='id')).all()
    if current_user.id == 1:
        # Pegar dados HTML para criar Rifas
        if request.method == 'POST':
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            qnty_cotas = request.form['quantidade']
            valor = request.form['valor']
            file = request.files['file']
            user = request.form['user']

            # Fazer Upload da imagem da rifa
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            try:
                print(filename)
            except:
                filename = 'padrão.jpg'

            # Tratar valores
            novo_valor = str(valor).replace(',', '.')

            # Passar valores para os campos do banco de dados "Rifa"
            bd_rifas = Rifa(titulo=titulo, descricao=descricao, qnty_cotas=qnty_cotas, valor=novo_valor, imagem=f'rifas/{filename}', criador=user)
            
            # Adicionar e commitar
            database.session.add(bd_rifas)
            database.session.commit()

            # Gerar a lista de números passando a quantidade
            numeros = criarCotas(int(qnty_cotas))
            
            # Pegar "id" da rifa que foi criada
            id = Rifa.query.filter_by(titulo=titulo, descricao=descricao, qnty_cotas=qnty_cotas, valor=novo_valor).first()
            
            # Percorrer lista de cotas geradas e adicionar as mesmas no banco de dados "Numero"
            for n in numeros:
                num = Numero(id_rifa=id.id, cota=int(n), valor=novo_valor)
                database.session.add(num)
                database.session.commit()

            # Retornar para a tela de criar rifas
            return redirect(url_for('criarrifas', id=1))
    else:
        # Redirecionar se o "id" não for do "adm"
        return redirect(url_for('login'))

    # Retornar o números reservados para Disponível
    

    return render_template('Rifa.html', rifas=rifas)
 
# Detalhes Rifas
@app.route('/detalhes/<int:id>', methods=['GET', 'POST'])
@login_required
def detalhes(id):
    # Formulário 
    form = FormEditarRifas()
    # Banco de Dados
    bd_rifas = Rifa.query.filter_by(id=id).first()
    # bd_numeros = Numero.query.filter_by(id_rifa=id).first()
    vendidos = Numero.query.filter_by(id_rifa=id, status='Pago').count()
    reservados = Numero.query.filter_by(id_rifa=id, status='Reservado').count()
    
    # Verificar requisição do form
    if request.method == 'POST':
                # Caso o botão acionado seja o "Alterar"
        if form.alterar.data == True:
            # Verificar campos preenchidos e alterar a rifa no banco de dados
            try:
                if form.sorteio.data != None:
                    bd_rifas.sorteio = form.sorteio.data
                    database.session.commit()
                    print(form.sorteio.data)
                
                if form.descricao.data != None and form.descricao.data != '':
                    bd_rifas.descricao = form.descricao.data
                    database.session.commit()
            except:
                pass
        
        # Gerar cotas premiadas e registar na descrição das rifas
        elif form.cota_premiada.data == True and form.qnty_cotas.data > 0:
            try:
                n_sorte = cotaPremiada(id, int(form.qnty_cotas.data))
                descricao = bd_rifas.descricao
                bd_rifas.descricao = f'{descricao}, Cota(s) premiadas{n_sorte}'
                database.session.commit()
            except:
                pass
        # Redirecionar
        return redirect(url_for('criarrifas', id=1))

    # Passar bancos de dados
    bd_numero = Numero.query.all()
    bd_usuario = Usuario.query.all()
    bd_pagamento = Pagamento.query.all()

    return render_template('Detalhes.html', rifas=bd_rifas, form=form, vendidos=vendidos, reservados=reservados, numeros=bd_numero, pagamentos=bd_pagamento, usuarios=bd_usuario)

# Comprar Rifa 
@app.route('/comprar/7617cc49242d36df96a604f9ccb8<int:id>afda66d931a981666451', methods=['GET', 'POST'])
def comprar(id):
    # Filtrar "id" no banco de dados "Rifa"
    bd_rifas = Rifa.query.filter_by(id=id).first()
    bd_usuarios = Usuario.query.all()
    
    vendidos = statusCotas(id, 'Pago')
    reservados = statusCotas(id, 'Reservado')
    disponiveis = statusCotas(id, 'Disponível')
    
    # Pegar dados do HTML
    if request.method == 'POST':
        id_rifa = request.form['id_rifa']
        qnty_cotas = request.form['quantidade']
        valor = request.form['preco']
        titulo = request.form['titulo']
        # Tratar Valor 
        novo_valor = str(valor).replace(',', '.')

        if novo_valor == '' or novo_valor == None or novo_valor == 'None':
            return redirect(url_for('comprar', id=id))

        #   Verificar se tem usuário logado
        return redirect(url_for('login', valor=novo_valor, titulo=titulo, cotas=qnty_cotas, id_rifa=id_rifa))
    return render_template('Comprar.html', pag='comprar', rifa=bd_rifas, vendido=vendidos, reservado=reservados, disponivel=disponiveis, usuarios=bd_usuarios)
  
# Pagamento
@app.route('/pagar/<valor>/<titulo>/<int:cotas>/<int:id_rifa>', methods=['GET'])
@login_required
def pagar(valor, titulo, cotas, id_rifa):
    try:
        id_cliente = current_user.id

        # Pegar Disponiveis
        cotas_disp = filtroCotas(id_rifa)

        # Pegar Cotas
        cotas_esc = pegarCotas(int(cotas), cotas_disp)
        print(f'essas são as cotas escolhidas:{cotas_esc}')

        # Criar função de pagamentos
        pag = criarPagamento(id_rifa, titulo, id_cliente, cotas_esc, valor)
        
        # Buscar o txid da transação
        txid = pag.get('txid') 

        # Criar função para atualizar dados no banco de cotas
        atualizarCotas(id_rifa, id_cliente, cotas_esc, txid=txid)
        
        return redirect(url_for('pagamento', valor=valor, txid=txid))
    except:
        return redirect(url_for('comprar', id=id_rifa))
    
@app.route('/pagamento/<valor>/<txid>', methods=['GET', 'POST'])
# @login_required
def pagamento(valor, txid):
    # Filtrar banco para pegar o qrcode
    bd_pagamentos = Pagamento.query.filter_by(txid=txid).first()

    if request.method == 'POST':
        return redirect(url_for('homepage'))
 
    return render_template('Pagamento.html', txid=f'qrcode/{txid}.jpeg', valor=valor, qrcode=bd_pagamentos.qrcode, pagamentos = bd_pagamentos, pag='pagamento')
 
# Visualizar Números
@app.route('/meusnumeros/637e11120c6c86c9bdeff49763136416915e91d158a88740', methods=['GET'])
@login_required
def numeros():
    id_cliente = current_user.id
    # Filtrar dados dos numeros comprados, baseados no "id_cliente"
    bd_numeros = Numero.query.filter_by(id_usuario=id_cliente, status='Pago').all()
    # Listas
    rifas = []
    # Percorrer a lista retornada
    for inf in bd_numeros:
        rifas.append(inf.id_rifa)

    # Tornar as rifas únicas 
    rifas_unicas = set(rifas)
 
    rifas = []
    
    # Filtrar banco de dados "Rifa", parâmetros "id_rifa" que está na lista
    for i in rifas_unicas:
        bd_rifas = Rifa.query.filter_by(id=i).first()
        rifas.append(bd_rifas)
    
    # Retornar o números reservados para Disponível
    

    return render_template('Numeros.html', rifas=rifas, numeros=bd_numeros) 

# Mostrar transações realizadas pelo "usuário", parâmetro "id_usuario"
@app.route('/transacoes/e9b6fa47855566b<int:id>41135ffd4a6b12eb624917ec66d4d1ef7', methods=['GET'])
@login_required
def transacoes(id): 
    bd_pagamentos = Pagamento.query.filter_by(id_usuario=id).order_by(desc(column='id')).all()
    
    # Retornar o números reservados para Disponível
    
    
    return render_template('Transacoes.html', pagamentos=bd_pagamentos)

@app.route('/suporte', methods=['POST', 'GET'])
def suporte():
    # Formulario 
    form = FormSuporte()
 
    # Filtrar chamados por usuário logado, mas se for o adm filtrar todos os chamados
    bd_suporte = Suporte.query.all()
    
    if request.method == 'POST':
        suporte = Suporte(id_usuario=1, descricao=form.descricao.data, status='Em Aberto', solucao='...')
        database.session.add(suporte)
        database.session.commit() 
    
    # Retornar o números reservados para Disponível
    

    return render_template('Suporte.html', suporte=bd_suporte, form=form)

@app.route('/webhook', methods=["POST"])
def imprimirWebhook():
    data = request.json
    
    txid = data.get('pix')[0].get('txid')
    endid = data.get('pix')[0].get('endToEndId')
    valor = data.get('pix')[0].get('valor')
    

    bd_pagamentos = Pagamento.query.filter_by(txid=txid).first()
    bd_pagamentos.endid = endid
    bd_pagamentos.status = 'Pagamento concluído'
    database.session.commit()

    bd_numeros = Numero.query.filter_by(id_pagamento=txid).all()

    # Percorrer a lista de números comprados
    for i in bd_numeros:    
        i.status = 'Pago'
        i.data_compra = datetime.now()
        database.session.commit()

    # Enviar uma requisição para a função pagamento
    response = requests.post(f'http://{request.host}/pagamento/{valor}/{txid}')
        # Verificar o usuário que está logado e enviar ele para outra pagina assim que o pagamento dele cair
    return 'pix ok'

 
# Escolher Cotas Premiadas ADM
# Minhas Rifas ADM

# Meus Números Visível
# Minhas Transações Visível
# Suporte Visível
# Pagamento Confirmado Visível

# Rota Gerar Cobranças 
