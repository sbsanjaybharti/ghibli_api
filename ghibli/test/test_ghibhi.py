#!/usr/bin/env python3
"""
Import packages
"""
import unittest
from flask import current_app
from base import BaseTestCase, existsin
from src.ghibhi import Ghibhi, BindMoviePeople


class TestGhibhiMethodExist(BaseTestCase):
    """Test the class exist status"""

    @existsin(Ghibhi)
    def test_class_have_method_films(self):
        """--> class:Ghibhi -> method:films exists"""

    @existsin(Ghibhi)
    def test_class_have_method_single_film(self):
        """--> class:Ghibhi -> method:single_film exists"""

    @existsin(Ghibhi)
    def test_class_have_method_peoples(self):
        """--> class:Ghibhi -> method:peoples exists"""


class TestBindMoviePeopleMethodExist(BaseTestCase):
    """Test the class exist status"""

    @existsin(BindMoviePeople)
    def test_class_have_method_film_ids(self):
        """--> class:BindMoviePeople -> method:film_ids exists"""

    @existsin(BindMoviePeople)
    def test_class_have_method_get_single(self):
        """--> class:BindMoviePeople -> method:get_single exists"""

    @existsin(BindMoviePeople)
    def test_class_have_method_get(self):
        """--> class:BindMoviePeople -> method:get exists"""


class TestGhibhiVariable(BaseTestCase):
    """Test class variable"""

    def test_class_variable_api_url(self):
        """--> class:Ghibhi -> variable:api_url exists"""
        api = Ghibhi()
        self.assertEqual(api.api_url, current_app.config['GHIBLI_API'])

    def test_class_variable_film_fields(self):
        """--> class:Ghibhi -> variable:film_fields exists"""
        api = Ghibhi()
        film_fields = ['id', 'title', 'director', 'producer', 'release_date', 'rt_score']

        status = 'id' in film_fields
        self.assertTrue(status)
        self.assertGreater(len(api.film_fields), 1)
        self.assertListEqual(list(api.film_fields), film_fields)

    def test_class_variable_people_fields(self):
        """--> class:Ghibhi -> variable:people_fields exists"""
        api = Ghibhi()
        people_fields = ['id', 'name', 'gender', 'age', 'eye_color', 'hair_color', 'films']

        status = 'id' in people_fields
        self.assertTrue(status)
        status = 'films' in people_fields
        self.assertTrue(status)
        self.assertGreater(len(api.film_fields), 2)
        self.assertListEqual(list(api.people_fields), people_fields)


class TestGhibhiMethod(BaseTestCase):
    """Test class methods"""

    def test_method_films(self):
        """--> class:Ghibhi -> method:films exists"""
        api = Ghibhi()
        response = api.films()
        self.assertIsInstance(response, object)
        self.assertEqual(type(response), list)
        self.assertGreater(len(response), 1)

    def test_method_single_film(self):
        """--> class:Ghibhi -> method:single_film exists"""
        api = Ghibhi()
        film_id = '5fdfb320-2a02-49a7-94ff-5ca418cae602'
        self.assertIsInstance(api.single_film(film_id), object)
        self.assertEqual(type(api.single_film(film_id)), dict)

    def test_method_people(self):
        """--> class:Ghibhi -> method:people exists"""
        api = Ghibhi()
        response = api.peoples()
        self.assertIsInstance(api.peoples(), object)
        self.assertEqual(type(api.peoples()), list)
        self.assertGreater(len(response), 1)


class TestBindMoviePeopleMethod(BaseTestCase):
    """Test class methods"""

    def test_method_film_ids(self):
        """--> class:Ghibhi -> method:film_ids exists"""
        obj = BindMoviePeople()
        response = obj.film_ids()
        self.assertEqual(type(response), list)
        self.assertGreater(len(response), 1)

    def test_method_get_single(self):
        """--> class:Ghibhi -> method:single_film exists"""
        obj = BindMoviePeople()
        response = obj.get_single('5fdfb320-2a02-49a7-94ff-5ca418cae602')

        self.assertNotEqual(response, None)
        self.assertGreater(len(response), 1)
        # self.assertEqual(type(response), list)
        self.assertIsInstance(len(response), object)

    def test_method_get(self):
        """--> class:Ghibhi -> method:people exists"""
        obj = BindMoviePeople()
        response = obj.get()

        self.assertNotEqual(response, None)
        self.assertGreater(len(response), 1)
        self.assertEqual(type(response), list)
        self.assertIsInstance(len(response), object)

        element = response.pop().keys()
        keys = ['id', 'title', 'director', 'producer', 'release_date', 'rt_score', 'people']
        self.assertListEqual(list(element), keys)
        self.assertGreater(len(element), 1)


if __name__ == '__main__':
    unittest.main()
