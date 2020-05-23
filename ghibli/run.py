import os
from flask import Flask, render_template, redirect, url_for
from flask_script import Manager
import unittest
import json
from pymemcache.client.base import Client
import datetime
from src.config import create_app
from src.service import service
from src.ghibhi import BindMoviePeople

# app = Flask(__name__)
app = create_app(os.getenv('APP_STATUS'))
manager = Manager(app)


@app.route('/')
def index():
    return redirect(url_for('movies'))

@app.route('/movies')
def movies():
    """
    Connect with memcache server
    """
    result = ''
    request = service()
    if request.status() is None:
        result = request.getFromServer()
    elif request.status() < 60:
        result = request.getFromCache()
    else:
        result = request.getCacheUpdate()

    response_object = {
        'code': 200,
        'type': 'Success',
        'data': result
    }
    return response_object

@manager.command
def run():
    app.run()


# Command: python run.py test
# Use to run Unit test
@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    manager.run()