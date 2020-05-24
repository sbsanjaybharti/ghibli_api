#!/usr/bin/env python3
"""
Import packages
"""
import os
import unittest
from flask import redirect, url_for, render_template
from flask_script import Manager
from src.config import create_app
from src.service import Service

# app = Flask(__name__)
app = create_app(os.getenv('APP_STATUS'))
manager = Manager(app)


@app.route('/')
def index():
    """
    Redirecting to movie page
    """
    return redirect(url_for('movies'))

@app.route('/movies')
def movies():
    """
    Connect with memcache server
    """
    request = Service()
    if request.status() is None:
        result = request.get_from_server()
    elif request.status() < 60:
        result = request.get_from_cache()
    else:
        result = request.get_cache_update()

    # Uncomment this line to show in json format
    # response_object = {
    #     'code': 200,
    #     'type': 'Success',
    #     'data': result
    # }
    return render_template('index.html', response=result, time=int(request.status()))

@manager.command
def create_cache():
    """
    Command: python run.py create
    Description: To run the application
    """
    print('Creating cache under process....')
    request = Service()
    if request.status() is None:
        request.get_from_server()
    elif request.status() < 60:
        request.get_from_cache()
    else:
        request.get_cache_update()
    print('Cache created successfully')

@manager.command
def run():
    """
    Command: python run.py run
    Description: To run the application
    """
    app.run()


# Command: python run.py test
# Use to run Unit test
@manager.command
def test():
    """
    Command: python run.py test
    Description: Runs the unit tests.
    """
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    manager.run()
