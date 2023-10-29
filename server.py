from webauthn import app
from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher

dispatch = PathInfoDispatcher({'/webauthn/v1': app})

server = WSGIServer(('0.0.0.0', 8080), dispatch)

try:
    server.start()
except (Exception, KeyboardInterrupt) as e:
    if not isinstance(e, KeyboardInterrupt):
        print(e)
    server.stop()
