import aiohttp
import aiohttp_jinja2

from aiohttp import web

class Landing(web.View):
    @aiohttp_jinja2.template('landing.html')
    async def get(self):
        return web.Response(content_type='application/json', text="main page")