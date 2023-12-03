import base64, json, requests, pyqrcode

from PIL import Image
from io import BytesIO
from datetime import datetime
from .models import Pagamento, Numero, database


URL_PROD = 'https://pix.api.efipay.com.br'
CLIENT_ID = 'Client_Id_963388fde5f5fb4911d337cc8411415131378e6e'
CLIENT_SECRET = 'Client_Secret_3721dba17535c050b41a1a6e3398fabe004fd6d6'
CERTIFICADO = 'FlaskRifas/cert/certificado.pem'
CHAVE = '6603223b-23aa-4a52-85ec-63a2fe05ec07'

class PixModel():
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {self.gerar_Token()}',
            'Content-Type': 'application/json',
            'x-skip-mtls-checking': 'true',
        }

    def gerar_Token(self):
        # Passar informações para acessar a API da efí
        auth = base64.b64encode(
            (f'{CLIENT_ID}:{CLIENT_SECRET}').encode()).decode()

        headers = {
            'Authorization': f"Basic {auth}",
            'Content-Type': 'application/json'
        }

        payload = {"grant_type": "client_credentials"}

        response = requests.post(
            f'{URL_PROD}/oauth/token', headers=headers, data=json.dumps(payload), cert=f'{CERTIFICADO}')

        # Retornar Token
        return json.loads(response.content)['access_token']

    def webhooks(self):
        body = {
            # "webhookUrl": "https://rifas.carlosdrifas.com/webhook"
            "webhookUrl": "https://cd.carlosdrifas.com/webhook?hmac=xyz&ignorar="
        }
        response = requests.put(f'{URL_PROD}/v2/webhook/{CHAVE}', data=json.dumps(body), headers=self.headers, cert=CERTIFICADO)
        response2 = requests.get(f'{URL_PROD}/v2/webhook/{CHAVE}', headers=self.headers,cert=CERTIFICADO)
        print(json.loads(response2.content))
        print()
        print(response.status_code, json.loads(response.content))
        return response

    def gerarCobranca(self, payload, id_rifa, id_cliente, lista_cotas):
        # Requisição sem txId
        response = requests.post(f'{URL_PROD}/v2/cob', data=json.dumps(payload), headers=self.headers, cert=CERTIFICADO)

        # Verificar status da requisição e retornar valor
        if response.status_code == 201:
            resp = json.loads(response.content)
            print(resp)
            # Abstrair resp
            txid = resp['txid']
            valor = resp['valor']['original']

            # Adicionar informações no Banco de Dados
            bd_pagamentos = Pagamento(id_rifa=id_rifa, id_usuario=id_cliente, cotas=str(lista_cotas), valor=valor, txid=txid, qnty_cotas=len(lista_cotas), data_pagamento=datetime.now())
            database.session.add(bd_pagamentos)
            database.session.commit()

            return resp

        # Retornar dicionário em branco
        return {}

    def gerarCobranca1(self, txid, payload):
        # Requisição com txId
        response = requests.put(f'{URL_PROD}/v2/cob/{txid}', data=json.dumps(payload), headers=self.headers, cert=CERTIFICADO)

        # Verificar status da requisição e retornar valor
        if response.status_code == 201:
            return json.loads(response.content)

        # Retornar dicionário em branco
        return {}

    def criarQrcode(self, location_id):
        # Requisição
        response = requests.get(f'{URL_PROD}/v2/loc/{location_id}/qrcode', headers=self.headers, cert=CERTIFICADO)

        # Retornar resposta
        return json.loads(response.content)

    def gerarQrcode(self, location_id, txid):
        # Chamar função
        code = self.criarQrcode(location_id)

        # Filtrar banco de dados
        bd_pagamentos = Pagamento.query.filter_by(txid=txid).first() 

        # Tratar resposta
        data_qrcode = code['qrcode']
        url = pyqrcode.QRCode(data_qrcode, error='H')
        url.png(f'FlaskRifas/static/qrcode/{txid}.jpeg', scale=3)
        img = Image.open(f'FlaskRifas/static/qrcode/{txid}.jpeg')
        # img = img.convert('RGBA')
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=100)
        img_io.seek(0)

        # Adicionar código qr no banco de dados
        bd_pagamentos.qrcode = data_qrcode

    def criarCobranca(self, payload, id_rifa, id_cliente, lista_cotas):
        # Gerar cobrança
        location_id = self.gerarCobranca(payload, id_rifa, id_cliente, lista_cotas)
        # Gerar QrCode
        
        qrcode = self.gerarQrcode(location_id['loc']['id'], location_id['txid'])
        return location_id

    def historicoPix(self):
        # Requisição
        response = requests.get(f'{URL_PROD}/v2/pix?inicio=2020-04-01T00:00:00Z&fim=2023-10-08T23:59:59Z', headers= self.headers, cert=CERTIFICADO)
        # Resposta
        resp = json.loads(response.content)
        return resp['pix']