from views.chat import Chat
from views.websocket import WebSocket
from views.auth import Login, SignIn

routes = [
    ('GET', '/',      Chat,      'chat'),
    ('GET', '/ws',    WebSocket, 'websocket'),
    ('*',   '/login', Login,     'login'),
    ('*',   '/signin',SignIn,    'signin')
]

def setupRoutes(app):
    for route in routes:
        app.router.add_route(route[0],route[1],route[2],name=route[3])
