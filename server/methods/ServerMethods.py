import json
from models import User
from utils.settings import clients


def send_client_message(user: User, message):
    """ Отправка сообщения пользователю """

    send_data = {
        'method': 'send_message',
        'params': {
            'msg': message,
        }
    }

    user.conn.send(
        bytes(json.dumps(send_data), encoding='UTF-8'),
    )


def send_client_message_to_all(message):
    """ Отправка сообщения всем пользователям """
    send_data = {
        'method': 'send_message',
        'params': {
            'msg': message,
        }
    }

    for user in clients.values():
        user.conn.send(
            bytes(json.dumps(send_data), encoding='UTF-8'),
        )
