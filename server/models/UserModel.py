from dataclasses import dataclass
import socket


@dataclass
class User:
    """ Модель сообщений """

    id: int
    name: str
    conn: socket
