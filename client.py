import json
import socket


sent_content = {
    'method': 'connection',
    'params': {
        'name': input('name: ')
    },
}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 7777))
sock.send(bytes(json.dumps(sent_content), encoding='UTF-8'))


def listen_server():
    """ Слушаем сервер """
    print(json.loads(sock.recv(2048)))
    return listen_server()


listen_server()

