import aiohttp
import aiohttp_jinja2

from aiohttp import web

from models import User, Message
from tools import redirect, set_redis

class Chat(web.View):
    
    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        redis = self.request.app['redis']
        if not await redis.get('user'):
            redirect(self.request, 'login')

class WebSocket(web.View):

    async def get(self):
        app = self.request.app
        redis = app['redis']
        
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        user_id = int(await redis.get('user'))
        user  = User(app,id=user_id)
        login = await user.get_login()
        print(f"{login} connect")

        for _ws in app['wslist']:
            await _ws.send_str(f'{login} joined')
        app['wslist'].append(ws)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    message_model = Message(app,author_id=user_id,text=msg.data)
                    await message_model.save_message() 
                    await self.broadcast(login,msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print("ws connection closed with exception %s" % ws.exception())

        app['wslist'].remove(ws)
        for _ws in app['wslist']:
            await _ws.send_str(f"{login} disconnected")

        return ws

    async def broadcast(self, login, msg):
        for peer in self.request.app['wslist']:
            await peer.send_str(f"{login}:{msg}")