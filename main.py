import requests
import os
import datetime
from flask import Flask, request, jsonify

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
INSTAGRAM_BUSINESS_ACCOUNT_ID = 'guisteps'
POST_ID = 'ID_DO_POST'
KEYWORD = 'palavra-chave'
LINK_TO_SEND = 'https://exemplo.com'

app = Flask(__name__)

@app.route('/')
def alive():
    now = datetime.datetime.now()
    return f'olá {now}'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        hub_verify_token = request.args.get('hub.verify_token')
        if hub_verify_token == 'SEU_TOKEN_DE_VERIFICACAO':
            return request.args.get('hub.challenge')
        return 'Token inválido', 403

    elif request.method == 'POST':
        data = request.json
        print(data)  
        return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(port=5000)

# Função para verificar comentários
def check_comments():
    print("Iniciando a aplicação...")
    print(f"Acess Token: {ACCESS_TOKEN}")
    url = f'https://graph.facebook.com/v12.0/{POST_ID}/comments'
    params = {
        'access_token': ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    comments = response.json().get('data', [])

    for comment in comments:
        if KEYWORD in comment['text']:
            user_id = comment['from']['id']
            send_dm(user_id, LINK_TO_SEND)

# Função para enviar mensagem direta
def send_dm(user_id, link):
    url = f'https://graph.facebook.com/v12.0/{user_id}/messages'
    params = {
        'access_token': ACCESS_TOKEN,
        'message': f'Aqui está o link que você pediu: {link}'
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        print(f'Mensagem enviada para {user_id}')
    else:
        print(f'Erro ao enviar mensagem: {response.text}')

# Executar a verificação de comentários
check_comments()