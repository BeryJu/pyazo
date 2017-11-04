import logging

import cherrypy
import django
from django.conf import settings
from django.db.utils import IntegrityError

from pyazo.wsgi import application


# pylint: disable=too-few-public-methods
class NullObject(object):
    """
    empty class to serve static files with cherrypy
    """
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
server = cherrypy._cpserver.Server()

server.socket_host = "0.0.0.0"
server.socket_port = 8000
server.thread_pool = 30
for key, value in settings.CHERRYPY_SERVER.items():
    setattr(server, key, value)
server.subscribe()

cherrypy.engine.start()
cherrypy.engine.block()
