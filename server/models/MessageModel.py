from dataclasses import dataclass

from datetime import datetime


@dataclass
class Message:
    """ Модель сообщений """

    text_msg: str
    date_send: datetime = datetime.now()
