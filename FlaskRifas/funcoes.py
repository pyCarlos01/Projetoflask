import os
import numpy as np

from random import *
from .models import *
from .api import *
from datetime import datetime

def criarCotas(quantidade):
    # Criar cotas
    cotas = np.arange(1, int(quantidade) + 1)

    # Retornar Valores
    return cotas

def filtroCotas(id_rifa):
    # Filtrar banco de dados "Numero", paramêtros "id_rifa" e "status"
    req = Numero.query.filter_by(id_rifa=id_rifa, status='Disponível').all()
    # Percorrer números com map e lambda e pegar o campo "cota" do banco de dados "Numero"
    num = map(lambda n: n.cota, req)

    # Retornar uma lista com os números "Disponível"
    return list(num)

def pegarCotas(qnty_cotas, lista):
    # O sample acaba embaralhando a lista e pegando a quantidade de elementos
    cotas_compradas = sample(lista, qnty_cotas)

    # Retornar uma lista com os números comprados
    return cotas_compradas
    
def criarPagamento(id_rifa, rifa, id_cliente, lista_cotas, valor):
    # Criar payload
    payload = {
      "calendario": {
        "expiracao": 600
      },
      "devedor": {
        "cpf": "47931393880",
        "nome": "Carlos Damião"
      },
      "valor": {
        "original": f"{valor}"
      },

      "chave": "6603223b-23aa-4a52-85ec-63a2fe05ec07",
      "solicitacaoPagador": f"{rifa}"
    }

    # Criar cobrança
    pix = PixModel()
    response = pix.criarCobranca(payload, id_rifa, id_cliente, lista_cotas)
    # Retornar cobrança
    return response

def atualizarCotas(id_rifa, id_cliente, lista_cotas, txid):
    # Loop
    print(f'{id_rifa}, {id_cliente}, {lista_cotas}, {txid}')
    for num in lista_cotas:
        # Filtrar banco de dados "Numero", parâmetros "id_rifa", "id_cliente" e "cota"
        bd_numeros = Numero.query.filter_by(id_rifa=id_rifa, cota=num).first()

        # Update e commit
        bd_numeros.status = 'Reservado'
        bd_numeros.id_usuario = id_cliente
        bd_numeros.id_pagamento = txid
        database.session.commit()
 
def cotaPremiada(id_rifa, qnty_cotas):
    # Pegar cotas disponíveis
    lista_disp = filtroCotas(id_rifa)

    # Gerar lista de cotas premiadas
    lista_final = pegarCotas(qnty_cotas, lista_disp)
     
    return lista_final

def reservados(status):
    # Filtrar o Banco de Números
    bd_numeros = Numero.query.filter_by(status=status).all()
    # Percorrer as cotas filtradas
    for i in bd_numeros:
        # Filtrar o Banco de Pagamentos
        bd_pagamentos = Pagamento.query.filter_by(txid=i.id_pagamento).all()
        # Tratar a data e hora de pagamento
        for j in bd_pagamentos:
            data = str(j.data_pagamento).replace(' ', '')
            momento_compra = datetime.strptime(data, f'%Y-%m-%d%H:%M:%S.%f')
            tempo = datetime.now() - momento_compra
            # Verificar se o tempo de pagamento é igual ou maior que 10 Min (600 seg)
            if tempo.days > 0 or tempo.seconds > 600:
                if status == 'Reservado':
                # Alterar o status, id_pagamento e id_usuario dos números no banco de Números
                    i.status = 'Disponível'
                    i.id_pagamento = ''
                    i.id_usuario = ''
                    database.session.commit()
                
                # Chamar Função para deletar qrcode
                deleteQrcode(j.txid)


def deleteQrcode(txid):
  # Definir caminho
  caminho = r'/static/qrcode/'
  arquivo = os.listdir(caminho)

  # Percorrer arquivos da pasta qrcode e verificar se existe aquele qrcode
  for arq in arquivo:
    if txid in arq:
      # Deletar
      os.remove(f'{caminho}{arq}')
    else:
        pass

def statusCotas(id_rifa, status):
  # Filtrar e contar
  bd_rifas = Numero.query.filter_by(id_rifa=id_rifa, status=status).count()

  return bd_rifas
  
def statusRifas(id_rifa):
    # Filtrar bancos
    vendidos = statusCotas(id_rifa, 'Pago')
    cotas = Rifa.query.filter_by(id=id_rifa).first()

    qnty_cotas = cotas.qnty_cotas
    # Verificar quantidade de vendidos e quantidade total da rifa
    if vendidos == qnty_cotas:
        bd_rifas = Rifa.query.filter_by(id=id_rifa).first()
        bd_rifas.status = 'Encerrado'
        # Chamar a função sorteio
        if bd_rifas.ganhador == 'A Definir':
            resposta = sorteio(id_rifa)
            bd_rifas.ganhador = f'Nome Ganhador: {resposta[0]}, Cota Sorteada: {resposta[1]}'
        # Salvar
        database.session.commit()
    else:
        pass

def sorteio(id_rifa):
    # Filtrar banco de dados Números
    bd_numeros = Numero.query.filter_by(id_rifa=id_rifa, status='Pago').all()
    # Percorrer números com map e lambda e pegar o campo "cota" do banco de dados "Numero"
    num = map(lambda n: n.cota, bd_numeros)
    # Sortear cota
    cota = pegarCotas(1, list(num))
    # Pegar id do ganhador
    id_usuario = Numero.query.filter_by(id_rifa=id_rifa, cota=cota[0]).first()
    # filtrar banco de dados usuario e pegar o nome do ganhador
    ganhador = Usuario.query.filter_by(id=id_usuario.id_usuario).first()
    # Retornar o ganhador
    return ganhador.nome, cota[0]
