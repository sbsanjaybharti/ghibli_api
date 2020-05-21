import os
from flask import Flask, render_template, redirect, url_for
from flask_script import Manager
import unittest
import json
from pymemcache.client.base import Client
import datetime
from src.config import create_app
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
    client = Client(('memcache', 11211))
    list_films = BindMoviePeople().get()
    return list_films
    # result = [
    #     {
    #         "id": row['id'],
    #         "title": row['title'],
    #         "description": row['description'],
    #         "director": row['director'],
    #         "producer": row['producer'],
    #         "release_date": row['release_date'],
    #         "rt_score": row['rt_score']
    #
    #     } for row in json.loads(list_films)]
    # # Create response for display
    # response_object = {
    #     'code': 200,
    #     'type': 'Success',
    #     'data': result
    # }
    # return response_object
    # check the cache creation time exist or not
    if client.get('movies_last_update') is None:
        # 1. Get all movies from ghibhi
        # 2. Add peoples to each movie
        # 3. Add data to movies_data and pass to memcache
        # 4. Add movies_last_update time to current time
        # 5. Add list of movies ID in movies_id list
        # 6. Return data
        return
    if (client.get('movies_last_update_time') - datetime.datetime.now()) > 1:
        # 1. Get movies ID from Ghibhi and compare with movies_id(cache)
        # 2. if both are same then
        #   i. update movies_last_update time to current time
        #   ii. get the movie data from movies_data(cache)
        # 3. if both are not same then
        #   i. Get the new movies id
        #   ii. get all the new movies with people and append the movies_data
        # 4. return movies_data
        return
    # return movies_data


    #Check the cache is older that one min
    #
    result = client.get('some_key')
    if result is None:
        client.set('some_key', [5, 6, 7, 8])
        result = client.get('some_key')
        return "Whale, Hello there!: {}".format(result)

    return "Whale, Hello there!: {}".format(result)

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