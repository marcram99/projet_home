from flask import Flask

from .main import app
from . import models


@app.cli.command('init_db')
def init_db():
    models.init_db()

@app.cli.command()
def hello():
    print('bonjour')