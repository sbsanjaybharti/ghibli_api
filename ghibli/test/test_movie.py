import unittest
from functools import wraps

from base import BaseTestCase
from src.ghibhi import movie

def existsin(namespace):
    """Given a namespace, this decorator asserts that an object with
    the same name as the function it's wrapping (minus ) exists in that
    namespace"""
    def wrapper(namedunittest):
        assert namedunittest.__name__.startswith('test_'), \
            "The wrapped '%s' function doesn't look like a unit test" % namedunittest.__name__

        @wraps(namedunittest)
        def inner(self, *args, **kwargs):
            self.assertTrue(hasattr(namespace, namedunittest.__name__.split('_')[1]))
            return namedunittest(self, *args, **kwargs)
        return inner
    return wrapper

class TestMovie(BaseTestCase):

    @existsin(movie)
    def test_get(self):
        """Testing the movie.get exists"""

    @existsin(movie)
    def test_people(self):
        """Testing the movie.get exists"""

    def test_class_is_object(self):
        film = None
        response = movie(film)
        self.assertIsInstance(response, object)

    def test_method_get_not_null(self):
        request = {
            "id": 'string',
            "title": 'string',
            "description": 'string',
            "director": 'string',
            "producer": 'string',
            "release_date": 'string',
            "rt_score": 'string',
        }
        response = movie(request)
        self.assertIsInstance(response.get(), object)

    def test_method_get_data(self):

        request = {
            "id": 'string',
            "title": 'string',
            "description": 'string',
            "director": 'string',
            "producer": 'string',
            "release_date": 'string',
            "rt_score": 'string',
        }
        response = movie(request)
        self.assertEqual(len(response.get()), len(response.film_fields))


if __name__ == '__main__':
    unittest.main()