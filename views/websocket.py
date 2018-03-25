import aiohttp
import aiohttp_jinja2
from aiohttp import web

class WebSocket(web.View):

    async def get(self):
        app = self.request.app

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        app.wslist.add(ws)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await self.broadcast(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print("ws connection closed woth exception %s" % ws.exception())
        
        print("Websocket connection closed")

        return ws

    async def broadcast(self, message):
        for peer in self.request.app.wslist:
            await peer.send_str(message)