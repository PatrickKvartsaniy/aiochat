import aiohttp
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session

class View(web.View):
    def __init__(self):
        pass

    @aiohttp_jinja2.template('index.html')
    async def index(self):
        return {"msg":"Hello world"}


async def ws_handler(request):
    
    app.wslist = set()

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app.wslist.add(ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print("ws connection closed woth exception %s" % ws.exception())
    
    print("Websocket connection closed")

    return ws

