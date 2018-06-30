import aiohttp
import aiohttp_jinja2
from aiohttp import web

from tools import redirect, set_redis

from auth.models import User
from chat.models import Message

class Login(web.View):
    @aiohttp_jinja2.template('login.html')  
    async def get(self):
        redis = self.request.app['redis']
        # print(await redis.get('user'))
        logged_in = await redis.get('user')
        if logged_in:
            await redirect(self.request, 'chat')
        return {'content':'Please login'}

    async def post(self):
        app  = self.request.app
        data = await self.request.json()
        user = User(app, nickname=data['nickname'], password=data['password'])
        result = await user.check_user()
        if result:
            await set_redis(app['redis'], self.request, user=result)
            return web.Response(content_type='application/json', text=str(result))

class SignIn(web.View):
    @aiohttp_jinja2.template('signin.html')
    async def get(self):
        redis = self.request.app['redis']
        if await redis.get('user'):
            await redirect(self.request, 'chat')
        return {'content':'Please enter your data'}

    async def post(self):
        app  = self.request.app
        data = await self.request.json()
        user = User(app, nickname=data['nickname'], email=data['email'], password=data['password'])
        result = await user.create_user()
        if result:
            await set_redis(app['redis'], result, self.request)
            await redirect(self.request, 'chat')
        return web.Response(content_type="application/json", text=str(result))

class Logout(web.View):
    async def get(self):
        redis = self.request.app['redis']
        if await redis.get('user'):
            await redis.delete('user')
            await redis.delete('channel')
            await redirect(self.request, 'login')
        else:
            await redirect(self.request, 'login')
