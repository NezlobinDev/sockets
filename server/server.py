import json
import socket
from threading import Thread

from utils.settings import clients, client_sockets
from models import User, Message
from methods import user_connection, user_disconnection, user_send_message


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.bind(('', 7777))
sock.listen(1000)


def listen_for_client(user: User):
    """ Прослушиваем подключенного клиента

    Открываемой поток, слушаем клиента до тех пор, пока он не отключится.
    При дисконнекте отправляем данные в метод `user_disconnection` - дальше работаем там.

    От клиента приходит схема вида:
    {
        # метод который будет вызывается
        'method': 'send_message',

        # параметры с которыми работаем
        'params': {

            # msg - сообщение пользователя
            'msg': 'string...',
        }
    }

    В зависимости от метода который пришел от клиента, вызываем нужный например - user_send_message
    """
    client = user.conn
    while True:
        try:
            data = json.loads(client.recv(1024)) # wqeqw
            if not data:
                continue
            print(data)
        except ConnectionResetError:
            if client in client_sockets:
                client_sockets.remove(client)
                del clients[user.id]
            user_disconnection(user)
            break

        method = data['method']
        if method == 'send_message':
            message = Message(text_msg=data['params']['msg'])
            user_send_message(user, message)


if __name__ == '__main__':
    """ Слушаем сервер, получаем подключаемых клиентов и авторизируем в системе 
    Отправим подключаемому клиенту информацию о том что подключение прошло успешно.
    
    Вызовем метод 'user_connection' - в дальнейшем, если потребуется выполнить какие то доп.действия
    при авторизации будем работать там.
    Для каждого пользователя открываем отдельный 'поток' в котором слушаем самого клиента.
    """
    print('start server')
    while True:
        client_socket, client_data = sock.accept()
        print(client_data)
        data = json.loads(client_socket.recv(1024))
        print(data)
        client_name = data['params']['name']
        client_data = (*client_data, client_name)
        print(f'[+] {tuple(client_data)} connected.')

        user_data = User(
            id=client_data[1],
            name=client_name,
            conn=client_socket,
            
        )

        clients.update({user_data.id: user_data})

        send_data = {
            'method': 'connection',
            'params': {
                'description': 'Успешно подключено',
                'client_id': user_data.id,
            }
        }

        client_socket.send(
            bytes(json.dumps(send_data), encoding='UTF-8'),
        )
        client_sockets.add(client_socket)
        user_connection(user_data)

        t = Thread(target=listen_for_client, args=(user_data, ))
        t.daemon = True
        t.start()
