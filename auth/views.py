from time import time

import aiohttp
import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import get_session

from models import User


def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    print(url)
    raise web.HTTPFound(url)


def set_session(session,user_id, request):
    session['user'] = str(user_id)
    session['last_visit'] = time()
    print(session)
    redirect(request, 'chat')


class Login(web.View):
    
    @aiohttp_jinja2.template('login.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'chat')
        return {'content':'Please login'}

    async def post(self):
        app, data = self.request.app, await self.request.json()
        user = User(app, nickname=data['nickname'], password=data['password'])
        result = await user.check_user()
        print(result)
        if result:
            session = await get_session(self.request)
            set_session(session, str(result), self.request)
        else:
            return web.Response(content_type='application/json', text=str(result))

class SignIn(web.View):

    @aiohttp_jinja2.template('signin.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'chat')
        return {'content':'Please enter your data'}

    async def post(self):
        app, data = self.request.app, await self.request.json()
        user = User(app, nickname=data['nickname'], email=data['email'], password=data['password'])
        result = await user.create_user()
        if result:
            session = await get_session(self.request)
            set_session(session, str(result), self.request)
        else:
            return web.Response(content_type="application/json", text=str(result))

class Logout(web.View):

    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
            redirect(self.request, 'login')
        else:
            raise web.HTTPForbidden(body=b'Forbidden')