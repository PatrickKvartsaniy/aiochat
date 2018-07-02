import asyncio
import aioredis

from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.redis_storage import RedisStorage

from settings import setupConfig, setupJinja, setupStatic
from routes import setupRoutes
from tools  import init_pg, shut_down

async def init(loop):
    #App init
    app = web.Application()

    #Add full configs
    app['config'] = setupConfig()

    #Add routes
    setupRoutes(app)
    app['wslist'] = {}

    #Add static config
    setupStatic(app)

    #Jinja config
    setupJinja(app)

    #PostgreSQL init
    app.db = await init_pg(app)

    #Setup redis
    REDIS_CONFIG = tuple(app['config']['redis'].values())
    redis_pool   = await aioredis.create_pool(REDIS_CONFIG, loop=loop)
    setup(app, RedisStorage(redis_pool))
    app['redis'] = await aioredis.create_redis(REDIS_CONFIG)

    return app

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app  = loop.run_until_complete(init(loop))
    handler = app.make_handler()

    server_generator = loop.create_server(handler, app['config']['HOST'],
                                                   app['config']['PORT'])
    server = loop.run_until_complete(server_generator)

    try:
        print(f"Start serving in {app['config']['HOST']}:{app['config']['PORT']}")
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(shut_down(server,app, handler))
        loop.close()
