import aiohttp
import aiohttp_jinja2

from aiohttp import web

from auth.models import User
from chat.models import Message, Friends

from tools import redirect, set_redis

class Chat(web.View):
    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        app = self.request.app
        redis = app['redis']
        usr = await redis.get('user')
        if not usr:
            await redirect(self.request, 'login')
        channel = self.request.match_info.get('channel') or 0
        await set_redis(redis, self.request,channel= channel)
        print(f"Connected to channel {channel}")
        login =   await User(app,id=int(usr)).get_login()
        friends =  await Friends(app,int(usr)).find_friends()
        print(friends)
        friends_names = [await User(app, id=id).get_login() for id in friends]
        return {'name':login, 'friends':friends_names}

class WebSocket(web.View):

    async def get(self):
        app = self.request.app
        redis = app['redis']
        
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        user_id = await redis.get('user')
        if not user_id:
           await redirect(self.request, 'login')
        login   = await User(app,id=int(user_id)).get_login()
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

        # for _ws in app['wslist'][self.channel_id]:
        #     await self.broadcast(login, "connected")

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

        # for _ws in app['wslist'][self.channel_id]:
        #     await self.broadcast(login, "disconnected")

        return ws

    async def broadcast(self, login, msg):
        room = self.request.app['wslist'][self.channel_id]
        for peer in room.values():
            await peer.send_str(f"{login}:{msg}")

class AddFriends(web.View):
    async def post(self):
        app = self.request.app
        data = await self.request.json()
        user = int(await app['redis'].get('user'))
        friend =  await User(app, nickname=data['nickname']).check_user()
        if friend:
            try:
                friends = Friends(app,user,friend)
                await friends.add_friends()
                resp = "Done"
            except Exception as e:
                print(f"Error: {e}, while making friends")
                resp = e
        else:
            resp = f"User {data['nickname']} does not exist"
            print(resp)
        return web.Response(content_type="application/json", text=resp)
