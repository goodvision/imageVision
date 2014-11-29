import sae
from myLife import wsgi

application = sae.create_wsgi_app(wsgi.application)
