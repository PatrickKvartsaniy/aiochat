import base64
import asyncio
import aioredis

from cryptography import fernet

from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.redis_storage import RedisStorage

from settings import setupConfig, setupJinja, setupStatic
from routes import setupRoutes
from tools import init_pg, close_pg, close_redis


loop = asyncio.get_event_loop()

async def init():
    #App init
    app = web.Application()

    #Add full configs
    app['config'] = setupConfig()

    #Add routes
    setupRoutes(app)
    app['wslist'] = []

    #Add static config
    setupStatic(app)

    #Jinja config
    setupJinja(app)

    #PostgreSQL init
    app.db = await init_pg(app)
    
    #Setup redis
    REDIS_CONFIG = tuple(app['config']['redis'].values())

    redis_pool = await aioredis.create_pool(REDIS_CONFIG, loop=loop)
    setup(app, RedisStorage(redis_pool))

    app['redis'] = await aioredis.create_redis(REDIS_CONFIG)

    #ShutDown setups
    app.on_shutdown.append(close_pg)
    app.on_shutdown.append(close_redis)

    return app

if __name__ == "__main__":
    app = loop.run_until_complete(init())
    web.run_app(app, 
                host=app['config']['host'],
                port=app['config']['port'])