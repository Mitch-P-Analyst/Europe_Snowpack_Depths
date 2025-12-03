# wsgi.py

from app.app import app

# Gunicorn will look for this object
server = app.server