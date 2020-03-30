import json
import functools
import asyncio    # delete when tests complete
from aiohttp import web

from db import read_message, create_message
from rabbitmq import rmq_send


async def get_message(request):
    """
    обрабатывает GET запрос и отдает json со статусом сообщения
    :param request:
    :return:
    """
    message_id = int(request.match_info.get('id'))
    message = await read_message(message_id)
    if message:
        text = 'Message status: {}'.format(message.status)
        print(text)
        body = {'status': message.status}
        return web.json_response(body, dumps=functools.partial(json.dumps, indent=4))
    else:
        return web.HTTPException(text='There is no message with such id.')


async def post_message(request):
    """
    обрабатывает POST запрос и возвращает статус обработки запроса и id сообщения в БД (пока в виде текста)
    :param request:
    :return:
    """
    message_json = await request.json()            # получаем  json body из сообщения, полученного методом POST
    message = await create_message(message_json)
    key = request.match_info.get('key')
    print('post_message method: ', message.status, message.id, message.message_body)

    await rmq_send(message, key)
    await asyncio.sleep(0.1)    # для того, чтобы воркер успел обновить статус сообщения в БД

    message = await read_message(message.id)
    if message:
        text = f'Message processing status: {message.status} \nMessage id: {message.id}'
    else:
        text = 'Message processing failed'
    print('updating message status: ', message.status, message.message_body)
    return web.Response(text=text)
