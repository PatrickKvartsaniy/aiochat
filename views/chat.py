import aiohttp
import aiohttp_jinja2
from aiohttp import web

class Chat(web.View):
    
    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        pass
