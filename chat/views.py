import aiohttp
import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import get_session

from models import User

class Chat(web.View):
    
    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        pass

class WebSocket(web.View):

    async def get(self):
        app = self.request.app

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        session = await get_session(self.request)
        print(session)
        user  = User(app,id=session.get('user'))
        login = await user.get_login()
        print(login)

        for ws in app['wslist']:
            await ws.send_str(f'{login} joined')
        
        app['wslist'].append(ws)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await self.broadcast(login,msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print("ws connection closed woth exception %s" % ws.exception())

        return ws

    async def broadcast(self, login, msg):
        for peer in self.request.app['wslist']:
            await peer.send_str(f"{login}:{msg}")