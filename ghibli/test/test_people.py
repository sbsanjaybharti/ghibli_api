import collections
import unittest
from flask import current_app

from base import BaseTestCase, existsin
from src.ghibhi import people

class TestPeopleMethodExist(BaseTestCase):

    @existsin(people)
    def test_class_have_method_group(self):
        """--> class:people -> method:group exists"""

    @existsin(people)
    def test_class_have_method_filter(self):
        """--> class:people -> method:filter exists"""

    @existsin(people)
    def test_class_have_method_bind(self):
        """--> class:people -> method:bind exists"""

class TestPeople(BaseTestCase):

    def test_pepole_group(self):
        """--> class:people -> method:group"""
        obj = people()
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
        """--> class:people -> method:filter"""
        obj = people()

        request = {
                  "films": [
                    "{}/{}/90b72513-afd4-4570-84de-a56c312fdf81".format(current_app.config['GHIBLI_API'], 'films'),
                    "{}/{}/ff24da26-a969-4f0e-ba1e-a122ead6c6e3".format(current_app.config['GHIBLI_API'], 'films')
                  ]
                }
        response = obj.filter(request)
        self.assertEqual(response, None)
    #
    # def test_pepole_bind_invalid_data(self):
    #     """--> class:people -> method:bind invalid data"""
    #     obj = people()
    #
    #     request = {'id':['a', 'b']}
    #     response = obj.bind(request)
    #     self.assertEqual(response, {'people': request})

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
        # response = response_object.getByfilmID(id)
        # self.assertIsNotNone(response)
        # self.assertIsInstance(response, object)
        # self.assertEqual(len(response[0]), len(response_object.people_fields)-1)

if __name__ == '__main__':
    unittest.main()