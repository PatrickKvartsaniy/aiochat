import base64
import asyncio
from cryptography import fernet

from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from settings import setupConfig, setupJinja, setupStatic
from routes import setupRoutes
from models import init_pg, close_pg


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

    #Setup middleware
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)

    setup(app, EncryptedCookieStorage(secret_key))

    return app


app = loop.run_until_complete(init())



if __name__ == "__main__":

    web.run_app(app, 
                host=app['config']['host'],
                port=app['config']['port'])