import os
import time
import asyncio
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from aio_pika.exceptions import CONNECTION_EXCEPTIONS

from db import init_pg, close_pg, read_message, update_message


user = os.environ.get('RABBITMQ_DEFAULT_USER')
password = os.environ.get('RABBITMQ_DEFAULT_PASS')
exchange = os.environ.get('RABBITMQ_EXCHANGE')
host = os.environ.get('RABBITMQ_HOST')

URL = f"amqp://{user}:{password}@{host}/"


async def on_message(message):
    """
    Функция-обработчик сообщения - подключается к бд и обновляет статус сообщения на 'processed'
    :param message:
    :return:
    """
    with message.process():
        print(" [x] %r:%r" % (message.routing_key, message.body.decode('utf-8')))
        db_message = await read_message(int(message.body.decode('utf-8')))
        print('Message: {}'.format(db_message.message_body))
        db_message = await update_message(int(message.body.decode('utf-8')))
        print('Message update: {}'.format(db_message.message_body))
        msg = db_message.message_body

        print(f'Message id: {db_message.id}')
        print(f'Message receiver: {msg["receiver"]}')
        print(f'Message body: {msg["body"]}')


async def main(loop):
    key = '33'

    try:
        # Perform connection
        print('connection:')
        connection = await connect_robust(URL, loop=loop)
        print('after connection')

        # Creating a channel
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        # Declare an exchange
        messages_exchange = await channel.declare_exchange(
            exchange, ExchangeType.DIRECT
        )

        # Declaring queue
        queue = await channel.declare_queue(f'{key}_queue', durable=True)

        # for binding_key in binding_keys:
        await queue.bind(messages_exchange, routing_key=key)

        # Start listening the queue with name 'task_queue'
        await queue.consume(on_message)
    # except ConnectionError:
    #     print('connection ERROR...')
    except Exception as exc:
        print('Connection Error... reconnecting after 5 seconds')
        time.sleep(5)
        await main(loop)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(init_pg())
    worker = loop.create_task(main(loop))

    # we enter a never-ending loop that waits for
    # data and runs callbacks whenever necessary.
    print(" [*] Waiting for messages. To exit press CTRL+C")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass  # Press Ctrl+C to stop
    finally:
        loop.run_until_complete(close_pg())
        worker.close()
        loop.close()
