import os
from gino import Gino


user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')
host = os.environ.get('POSTGRES_HOST')

URL = f'postgresql://{user}:{password}@{host}:5432/{db_name}'

db = Gino()


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.String(20))
    message_body = db.Column(db.JSON())


async def init_pg():
    print('initializing DataBase...')
    await db.set_bind(URL)
    await db.gino.create_all()
    print('Done')


async def close_pg():
    await db.pop_bind().close()


async def create_message(message_json):
    print('create message method')
    message = await Messages.create(status='received', message_body=message_json)
    print('created message: ', message.id)
    return message


async def read_message(message_id):
    print('read message method')
    print('id: {}'.format(message_id))
    message = await Messages.query.where(Messages.id == message_id).gino.one_or_none()

    if message:
        print('read message method message: ', message.id, message.status, message.message_body)
        return message
    else:
        return message


async def update_message(message_id):
    print('update message method')
    message = await Messages.get(message_id)
    await message.update(status='processed').apply()
    message = await Messages.get(message_id)
    print('message updated:', message.status)
    return message