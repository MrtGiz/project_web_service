from aiohttp import web
from routes import setup_routes
from db import init_pg, close_pg


if __name__ == '__main__':
    app = web.Application()
    setup_routes(app)
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    web.run_app(app)
