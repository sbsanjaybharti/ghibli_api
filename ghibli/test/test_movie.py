#!/usr/bin/env python3
"""
Import packages
"""
import unittest
from functools import wraps

from base import BaseTestCase, existsin
from src.ghibhi import Movie, People


class TestMovieMethodExist(BaseTestCase):
    """Test the class exist status"""

    @existsin(Movie)
    def test_class_have_method_get(self):
        """--> class:Movie -> method:get exists"""

    @existsin(Movie)
    def test_class_have_method_people(self):
        """--> class:Movie -> method:people exists"""

class TestMovie(BaseTestCase):
    """Test class methods"""

    def test_class_is_object(self):
        """--> class:Movie -> variable:film if null"""
        film = None
        response = Movie(film)
        self.assertIsInstance(response, object)

    def test_method_get_null(self):
        """--> class:Movie -> method:get null value"""
        response = Movie()
        self.assertEqual(response.get(), {})

    def test_method_get_not_null(self):
        """--> class:Movie -> method:get not null value"""
        request = {
            "id": 'string',
            "title": 'string',
            "description": 'string',
            "director": 'string',
            "producer": 'string',
            "release_date": 'string',
            "rt_score": 'string',
        }
        obj = Movie(request)
        response = obj.get()
        self.assertIsInstance(response, object)
        self.assertListEqual(list(response.keys()), obj.film_fields)

    def test_method_get_data(self):
        """--> class:Movie -> method:get value"""
        request = {
            "id": 'string',
            "title": 'string',
            "description": 'string',
            "director": 'string',
            "producer": 'string',
            "release_date": 'string',
            "rt_score": 'string',
        }
        obj = Movie(request)
        response = obj.get()
        self.assertEqual(len(response), len(obj.film_fields))
        self.assertListEqual(list(response.keys()), obj.film_fields)

    def test_method_people_class_parameter(self):
        """--> class:Movie -> method:people with class parameter"""
        request = {
            "id": 'string',
            "title": 'string',
            "description": 'string',
            "director": 'string',
            "producer": 'string',
            "release_date": 'string',
            "rt_score": 'string',
        }
        response = Movie(request).people()
        self.assertIsInstance(response, object)
    def test_method_people_by_parameter(self):
        """--> class:Movie -> method:people with method parameter"""
        request = '5fdfb320-2a02-49a7-94ff-5ca418cae602'
        # response = Movie()
        response = Movie().people(request)
        self.assertIsInstance(response, object)

if __name__ == '__main__':
    unittest.main()
