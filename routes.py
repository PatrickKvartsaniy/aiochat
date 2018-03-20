from views import View, ws_handler

routes = [
    ('GET', '/', View.index, 'main'),
    ('GET', '/ws', ws_handler, 'websocket')
]

def setupRoutes(app):
    for route in routes:
        app.router.add_route(route[0],route[1],route[2],name=route[3])