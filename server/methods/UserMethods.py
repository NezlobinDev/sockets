from models import Message, User

from .ServerMethods import send_client_message_to_all


def user_connection(user: User):
    """ Метод срабатывающий при подключении клиента """
    send_client_message_to_all(f'Подключился: {user.name}({user.id})')


def user_disconnection(user: User):
    """ Метод срабатывающий при отключении клиента """
    send_client_message_to_all(f'Отключился: {user.name}({user.id})')


def user_send_message(user: User, msg: Message):
    """ Метод срабатывающий при отправке сообщения в чат """

    # отправим сообщение всем подключенным пользователям
    send_client_message_to_all(f'{user.name}({user.id}): {msg.text_msg}')
