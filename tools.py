from time import time

from aiohttp import web

import aiopg.sa

async def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    print(url)
    raise web.HTTPFound(url)


async def set_redis(redis,request,user=None,channel=None):
    if user:
        await redis.set('user',str(user))
        await redis.set('last_visit',time())
        await redirect(request, 'chat')
    elif channel:
        await redis.set('channel', channel)

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

# async def close_ws(app):
#     for ws in app['wslist']:
#         ws.close(code=101, message='Server shutdown')

async def shut_down(server, app, handler):
    server.close()
    await server.wait_closed()
    await close_pg(app)
    await close_redis(app)
    await app.shutdown()
    await handler.shutdown()
    await app.cleanup()