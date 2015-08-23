import sae

from zgvl import wsgi

application = sae.create_wsgi_app(wsgi.application)
