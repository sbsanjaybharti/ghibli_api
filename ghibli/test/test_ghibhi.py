import unittest
from base import BaseTestCase
from src.ghibhi import ghibhi

class TestGhibhiAPI(BaseTestCase):

    def test_api_url_equal_to_ghibhi(self):
        api = ghibhi()
        self.assertEqual(api.api_url, 'https://ghibliapi.herokuapp.com')

    def test_films_method_is_object_type(self):
        api = ghibhi()
        self.assertIsInstance(api.films(), object)

    def test_people_method_is_object_type(self):
        api = ghibhi()
        self.assertIsInstance(api.films(), object)

if __name__ == '__main__':
    unittest.main()