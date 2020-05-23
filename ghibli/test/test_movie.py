import unittest
from functools import wraps

from base import BaseTestCase, existsin
from src.ghibhi import movie


class TestGhibhiMethodExist(BaseTestCase):

    @existsin(movie)
    def test_class_have_method_get(self):
        """--> class:movie -> method:get exists"""

    @existsin(movie)
    def test_class_have_method_people(self):
        """--> class:movie -> method:people exists"""

class TestMovie(BaseTestCase):

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

    def test_method_get_ID(self):
        request = '5fdfb320-2a02-49a7-94ff-5ca418cae602'
        # response = movie()
        response = movie().people(request)
        print(response)
        pass

if __name__ == '__main__':
    unittest.main()