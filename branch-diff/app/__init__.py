"""
author: Pro Arhant
Automate git ops and the rest...

"""

from flask import Flask

def create_app():
  app = Flask(__name__)
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  return app

app = create_app()
from app import views
