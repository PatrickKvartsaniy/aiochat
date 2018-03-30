from time import time

from aiohttp import web

import aiopg.sa

async def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    return web.HTTPFound(url)


async def set_redis(redis,user,request):
    await redis.set('user',str(user))
    await redis.set('last_visit',time())
    await redirect(request, 'chat')

async def close_redis(app):
        app['redis'].close()

async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    return engine

async def close_pg(app):
    app.db.close()
    await app.db.wait_closed()