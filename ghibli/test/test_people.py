#!/usr/bin/env python3
"""
Import packages
"""
import collections
import unittest
from flask import current_app

from base import BaseTestCase, existsin
from src.ghibhi import People


class TestPeopleMethodExist(BaseTestCase):
    """Test the class exist status"""

    @existsin(People)
    def test_class_have_method_group(self):
        """--> class:People -> method:group exists"""

    @existsin(People)
    def test_class_have_method_filter(self):
        """--> class:People -> method:filter exists"""

    @existsin(People)
    def test_class_have_method_bind(self):
        """--> class:People -> method:bind exists"""


class TestPeople(BaseTestCase):
    """Test class methods"""

    def test_pepole_group(self):
        """--> class:People -> method:group"""
        obj = People()
        #
        # request = {
        #           "id": "6b3facea-ea33-47b1-96ce-3fc737b119b8",
        #           "name": "Renaldo Moon aka Moon aka Muta",
        #           "gender": "Male",
        #           "age": "NA",
        #           "eye_color": "White",
        #           "hair_color": "Beige",
        #           "films": [
        #             "https://ghibliapi.herokuapp.com/films/90b72513-afd4-4570-84de-a56c312fdf81",
        #             "https://ghibliapi.herokuapp.com/films/ff24da26-a969-4f0e-ba1e-a122ead6c6e3"
        #           ]
        #         }
        response = obj.group()
        self.assertIsInstance(response, object)
        self.assertEqual(type(response), collections.defaultdict)
        self.assertGreater(len(response), 1)

    def test_pepole_filter(self):
        """--> class:People -> method:filter"""
        obj = People()

        request = {
            "films": [
                "{}/{}/90b72513-afd4-4570-84de-a56c312fdf81".format(
                    current_app.config['GHIBLI_API'],
                    'films'),
                "{}/{}/ff24da26-a969-4f0e-ba1e-a122ead6c6e3".format(
                    current_app.config['GHIBLI_API'],
                    'films')
            ]
        }
        response = obj.filter(request)
        self.assertEqual(response, None)


if __name__ == '__main__':
    unittest.main()
