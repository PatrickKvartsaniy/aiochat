from chat.views    import Chat, WebSocket, AddFriends
from auth.views    import Login, SignIn, Logout
from landing.views import Landing

routes = [
    ('GET', '/',              Landing,   'landing'),
    ('GET', '/chat',          Chat,      'chat'),
    ('GET', '/chat/{channel}',Chat,      'chatroom'),
    ('GET', '/ws',            WebSocket, 'websocket'),
    ('GET', '/ws/{channel}',  WebSocket, 'channel'),
    ('POST','/friends',       AddFriends,'friends'),
    ('*',   '/login',         Login,     'login'),
    ('*',   '/signin',        SignIn,    'signin'),
    ('*',   '/logout',        Logout,    'logout')
]

def setupRoutes(app):
    for route in routes:
        app.router.add_route(route[0],route[1],route[2],name=route[3])