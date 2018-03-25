from aiohttp import web
from settings import setupConfig, setupJinja, setupStatic
from routes import setupRoutes
from models import init_pg, close_pg

import asyncio

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

    return app


app = loop.run_until_complete(init())



if __name__ == "__main__":

    web.run_app(app, 
                host=app['config']['host'],
                port=app['config']['port'])