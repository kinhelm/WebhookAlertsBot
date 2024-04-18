import requests
from datetime import datetime
from flask import Flask, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from models.User import User

engine = create_engine("sqlite:///mydb.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

import keys

TELEGRAM_BOT_TOKEN = keys.token

app = Flask(__name__)


def broadcast_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    chat_ids = list(set(get_all_chat_ids()))
    for chat_id in chat_ids:
        payload = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(url, json=payload)
        print(response.json())


def get_all_chat_ids():
    chat_ids = session.query(User.chat_id).all()
    return [chat_id[0] for chat_id in chat_ids]


@app.route('/push-alert', methods=['POST'])
def newrelic_alert():
    data = request.json
    alert_message = data['message']
    current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    message = f'\U0001f558 {current_time}\n{alert_message}'
    broadcast_message(message)
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
