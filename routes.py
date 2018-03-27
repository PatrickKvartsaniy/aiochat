from chat.views import Chat, WebSocket
from auth.views import Login, SignIn, Logout

routes = [
    ('GET', '/',        Chat,     'chat'),
    ('GET', '/ws',      WebSocket,'websocket'),
    ('*',   '/login',   Login,    'login'),
    ('*',   '/signin',  SignIn,   'signin'),
    ('GET', '/logout',  Logout,   'logout'),
]

def setupRoutes(app):
    for route in routes:
        app.router.add_route(route[0],route[1],route[2],name=route[3])