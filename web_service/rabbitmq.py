import os
from aio_pika import connect, Message, DeliveryMode, ExchangeType


user = os.environ.get('RABBITMQ_DEFAULT_USER')
password = os.environ.get('RABBITMQ_DEFAULT_PASS')
exchange = os.environ.get('RABBITMQ_EXCHANGE')
host = os.environ.get('RABBITMQ_HOST')

URL = f"amqp://{user}:{password}@{host}/"


async def rmq_send(message, key):
    """
    Создает подключение к RabbitMQ, создает exchange типа direct и отсылает в него id сообщения, хранящегося в БД
    :param message:
    :param key:
    :return None:
    """

    # Perform connection
    connection = await connect(URL)

    # Creating a channel
    channel = await connection.channel()
    messages_exchange = await channel.declare_exchange(exchange, ExchangeType.DIRECT)

    routing_key = key

    message_body = str(message.id).encode('utf-8')

    rmq_message = Message(message_body, delivery_mode=DeliveryMode.PERSISTENT)

    await messages_exchange.publish(rmq_message, routing_key=routing_key)

    print(" [x] Sent %r" % rmq_message)
    print('rmq message body:', rmq_message.body.decode('utf-8'))

    await connection.close()
