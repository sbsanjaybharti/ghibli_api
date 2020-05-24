import unittest
from functools import wraps

from base import BaseTestCase, existsin
from src.ghibhi import movie, people


class TestMovieMethodExist(BaseTestCase):

    @existsin(movie)
    def test_class_have_method_get(self):
        """--> class:movie -> method:get exists"""

    @existsin(movie)
    def test_class_have_method_people(self):
        """--> class:movie -> method:people exists"""

class TestMovie(BaseTestCase):

    def test_class_is_object(self):
        """--> class:movie -> variable:film if null"""
        film = None
        response = movie(film)
        self.assertIsInstance(response, object)

    def test_method_get_null(self):
        """--> class:movie -> method:get null value"""
        response = movie()
        self.assertEqual(response.get(), {})

    def test_method_get_not_null(self):
        """--> class:movie -> method:get not null value"""
        request = {
            "id": 'string',
            "title": 'string',
            "description": 'string',
            "director": 'string',
            "producer": 'string',
            "release_date": 'string',
            "rt_score": 'string',
        }
        obj = movie(request)
        response = obj.get()
        self.assertIsInstance(response, object)
        self.assertListEqual(list(response.keys()), obj.film_fields)

    def test_method_get_data(self):
        """--> class:movie -> method:get value"""
        request = {
            "id": 'string',
            "title": 'string',
            "description": 'string',
            "director": 'string',
            "producer": 'string',
            "release_date": 'string',
            "rt_score": 'string',
        }
        obj = movie(request)
        response = obj.get()
        self.assertEqual(len(response), len(obj.film_fields))
        self.assertListEqual(list(response.keys()), obj.film_fields)

    def test_method_people_class_parameter(self):
        """--> class:movie -> method:people with class parameter"""
        request = {
            "id": 'string',
            "title": 'string',
            "description": 'string',
            "director": 'string',
            "producer": 'string',
            "release_date": 'string',
            "rt_score": 'string',
        }
        response = movie(request).people()
        self.assertIsInstance(response, object)
    def test_method_people_by_parameter(self):
        """--> class:movie -> method:people with method parameter"""
        request = '5fdfb320-2a02-49a7-94ff-5ca418cae602'
        # response = movie()
        response = movie().people(request)
        self.assertIsInstance(response, object)

if __name__ == '__main__':
    unittest.main()