#Credits to https://github.com/arskom/spyne/tree/master/examples/flask which acted as the base for this assignment

#!/usr/bin/env python
# encoding: utf8

from werkzeug.wsgi import DispatcherMiddleware
from spyne.server.wsgi import WsgiApplication

from apps import spyned
from apps.flasked import app


# SOAP services are distinct wsgi applications, we should use dispatcher
# middleware to bring all aps together
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '': WsgiApplication(spyned.create_app(app))
})

if __name__ == '__main__':
    app.run()
