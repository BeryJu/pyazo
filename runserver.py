"""pyazo cherrypy server"""
import cherrypy
from django.conf import settings

from pyazo.wsgi import application


# pylint: disable=too-few-public-methods
class NullObject:
    """empty class to serve static files with cherrypy"""
    pass


cherrypy.config.update({'log.screen': True,
                        'log.access_file': '',
                        'log.error_file': ''
                       })
cherrypy.tree.graft(application, '/')
# Mount NullObject to serve static files
cherrypy.tree.mount(NullObject(), '/static', config={
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': settings.STATIC_ROOT,
    }
})
cherrypy.server.unsubscribe()
# pylint: disable=protected-access
SERVER = cherrypy._cpserver.Server()

SERVER.socket_host = "0.0.0.0"
SERVER.socket_port = 8000
SERVER.thread_pool = 30
for key, value in settings.CHERRYPY_SERVER.items():
    setattr(SERVER, key, value)
SERVER.subscribe()

cherrypy.engine.start()
cherrypy.engine.block()
