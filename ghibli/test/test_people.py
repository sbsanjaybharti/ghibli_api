import unittest
from functools import wraps

from base import BaseTestCase
from src.ghibhi import people

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

class TestPeople(BaseTestCase):

    @existsin(people)
    def test_get(self):
        """Testing the movie.get exists"""

    @existsin(people)
    def test_getByfilmID(self):
        """Testing the movie.get exists"""

    @existsin(people)
    def test_bind(self):
        """Testing the movie.get exists"""

    def test_pepole_get_data(self):
        id = "58611129-2dbc-4a81-a72f-77ddfc1b1b49"
        # films = {
        #     'id': "ba924631-068e-4436-b6de-f3283fa848f0",
        #     'name': "Ashitaka",
        #     'gender': "Male",
        #     'age': "late teens",
        #     'eye_color': "Brown",
        #     'hair_color': "Brown"
        # }
        films = {
            "id": 'string',
            "title": 'string',
            "description": 'string',
            "director": 'string',
            "producer": 'string',
            "release_date": 'string',
            "rt_score": 'string',
        }
        response_object = people()
        response = response_object.getByfilmID(id)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, object)
        self.assertEqual(len(response[0]), len(response_object.people_fields)-1)

if __name__ == '__main__':
    unittest.main()