from aiohttp import web
from settings import setupConfig, setupJinja, setupStatic
from routes import setupRoutes
from models import init_pg, close_pg


def init():
    #App init
    app = web.Application()
    
    #Add full configs
    setupConfig(app)
    
    #Add routes
    setupRoutes(app)

    #Add static config
    setupStatic(app)

    #Jinja config
    setupJinja(app)
    
    #PostgreSQL init
    init_pg(app)

    return app

app = init()

if __name__ == "__main__":
    web.run_app(app, 
                host=app.config['host'],
                port=app.config['port'])