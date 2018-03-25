import aiohttp
import aiohttp_jinja2
from aiohttp import web

from models import User



class Login(web.View):
    
    @aiohttp_jinja2.template('login.html')
    async def get(self):
        pass

    async def post(self):
        app, data = self.request.app, await self.request.json()
        user = User(app, data['nickname'],data['password'])
        result = await user.check_user()
        print(result)
        return web.Response(content_type="application/json", text="hello")

class SignIn(web.View):

    @aiohttp_jinja2.template('signin.html')
    async def get(self):
        pass

    async def post(self):
        app, data = self.request.app, await self.request.json()
        user = User(app, data['nickname'],data['email'],data['password'])
        result = await user.create_user()
        return web.Response(content_type="application/json", text=str(result))