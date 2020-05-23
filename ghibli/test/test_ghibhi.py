import unittest
from flask import current_app
from base import BaseTestCase, existsin
from src.ghibhi import ghibhi

class TestGhibhiMethodExist(BaseTestCase):

    @existsin(ghibhi)
    def test_class_have_method_films(self):
        """--> class:ghibhi -> method:films exists"""

    @existsin(ghibhi)
    def test_class_have_method_singleFilm(self):
        """--> class:ghibhi -> method:singleFilm exists"""

    @existsin(ghibhi)
    def test_class_have_method_people(self):
        """--> class:ghibhi -> method:people exists"""

class TestGhibhiVariable(BaseTestCase):

    def ghibhi(self):
        return ghibhi()

    def test_class_variable_api_url(self):
        """--> class:ghibhi -> variable:api_url exists"""
        api = self.ghibhi()
        self.assertEqual(api.api_url, current_app.config['GHIBLI_API'])

    def test_class_variable_film_fields(self):
        """--> class:ghibhi -> variable:film_fields exists"""
        api = self.ghibhi()
        film_fields = ['id', 'title', 'director', 'producer', 'release_date', 'rt_score']

        status = True if 'id' in film_fields else False
        self.assertTrue(status)
        self.assertGreater(len(api.film_fields), 1)
        self.assertListEqual(list(api.film_fields), film_fields)

    def test_class_variable_people_fields(self):
        """--> class:ghibhi -> variable:people_fields exists"""
        api = self.ghibhi()
        people_fields = ['id', 'name', 'gender', 'age', 'eye_color', 'hair_color', 'films']

        status = True if 'id' in people_fields else False
        self.assertTrue(status)
        status = True if 'films' in people_fields else False
        self.assertTrue(status)
        self.assertGreater(len(api.film_fields), 2)
        self.assertListEqual(list(api.people_fields), people_fields)

class TestGhibhiMethod(BaseTestCase):

    def test_method_films(self):
        """--> class:ghibhi -> method:films exists"""
        api = self.ghibhi()
        response = api.films()
        self.assertIsInstance(response, object)
        self.assertEqual(type(response), list)
        self.assertGreater(len(response), 1)

    def test_method_singleFilm(self):
        """--> class:ghibhi -> method:singleFilm exists"""
        api = self.ghibhi()
        id = '5fdfb320-2a02-49a7-94ff-5ca418cae602'
        self.assertIsInstance(api.singleFilm(id), object)
        self.assertEqual(type(api.singleFilm(id)), dict)

    def test_method_people(self):
        """--> class:ghibhi -> method:people exists"""
        api = self.ghibhi()
        response = api.people()
        self.assertIsInstance(api.people(), object)
        self.assertEqual(type(api.people()), list)
        self.assertGreater(len(response), 1)

if __name__ == '__main__':
    unittest.main()