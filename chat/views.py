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
        channel = self.request.match_info.get('channel')
        if channel:
            await set_redis(redis, self.request, channel=channel)
        print(f"Connected to channel {channel}")

class WebSocket(web.View):

    async def get(self):
        app = self.request.app
        redis = app['redis']
        
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        user_id = int(await redis.get('user'))
        user = User(app,id=user_id)
        login = await user.get_login()

        channel = await redis.get('channel')
        try:
            self.channel_id = channel.decode('utf-8')
        except AttributeError:
            self.channel_id = 0

        try:
            app['wslist'][self.channel_id][login] = ws
        except KeyError:
            app['wslist'][self.channel_id] = {}
            app['wslist'][self.channel_id][login] = ws
        
        print(f"{login} connect to room {self.channel_id}")

        for _ws in app['wslist'][self.channel_id]:
            await self.broadcast(login, "connected")

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

        app['wslist'].pop(login, None)
        for _ws in app['wslist'][self.channel_id]:
            await self.broadcast(login, "disconnected")

        return ws

    async def broadcast(self, login, msg):
        room = self.request.app['wslist'][self.channel_id]
        for peer in room.values():
            await peer.send_str(f"{login}:{msg}")