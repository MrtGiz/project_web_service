from aiohttp import web
from views import get_message, post_message


def setup_routes(app):
    app.add_routes([web.get('/messages/{id}', get_message),
                    web.post('/webhook/{key}', post_message),
                    ])
