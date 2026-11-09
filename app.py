"""
WSGI Application entrypoint alias for Render / Cloud hosting.
Exposes 'application' and 'app' pointing to config.wsgi.application.
"""
from config.wsgi import application

app = application
