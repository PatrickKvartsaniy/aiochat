from time import time

import aiohttp
import aiohttp_jinja2
from aiohttp import web

from models import User


async def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    return web.HTTPFound(url)


async def set_redis(redis,user,request):
    await redis.set('user',str(user))
    await redis.set('last_visit',time())
    await redirect(request, 'chat')

class Login(web.View):
    @aiohttp_jinja2.template('login.html')
    async def get(self):
        return {'content':'Please login'}

    async def post(self):
        app  = self.request.app
        data = await self.request.json()
        user = User(app, nickname=data['nickname'], password=data['password'])
        result = await user.check_user()
        if result:
            await set_redis(app['redis'], result, self.request)
            return web.Response(content_type='application/json', text=str(result))

class SignIn(web.View):

    @aiohttp_jinja2.template('signin.html')
    async def get(self):
        return {'content':'Please enter your data'}

    async def post(self):
        app  = self.request.app
        data = await self.request.json()
        user = User(app, nickname=data['nickname'], email=data['email'], password=data['password'])
        result = await user.create_user()
        if result:
            await set_redis(app['redis'], result, self.request)
            await redirect(self.request, 'chat')
        else:
            return web.Response(content_type="application/json", text=str(result))

class Logout(web.View):

    async def get(self):
        # session = await get_session(self.request)
        # if session.get('user'):
        #     del session['user']
        #     redirect(self.request, 'login')
        # else:
        #     raise web.HTTPForbidden(body=b'Forbidden')
        pass