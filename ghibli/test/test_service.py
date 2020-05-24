#!/usr/bin/env python3
"""
Import packages
"""
import unittest
from time import time, sleep
from flask import current_app
from base import BaseTestCase, existsin
from src.service import Service, Cache


class TestServiceMethodExist(BaseTestCase):
    """Test the class exist status"""

    @existsin(Service)
    def test_class_have_method_status(self):
        """--> class:Service -> method:status exists"""

    @existsin(Service)
    def test_class_have_method_get_from_server(self):
        """--> class:Service -> method:get_from_server exists"""

    @existsin(Service)
    def test_class_have_method_get_from_cache(self):
        """--> class:Service -> method:get_from_cache exists"""

    @existsin(Service)
    def test_class_have_method_get_cache_update(self):
        """--> class:Service -> method:get_cache_update exists"""


class TestServiceMethods(BaseTestCase):
    """Test class methods"""

    # class to test status function
    def test_method_status_null(self):
        """--> class:Service -> method:status value can be null"""

        self.assertEqual(Service().status(), None)

    def test_method_status_not_null(self):
        """--> class:service -> method:status can have value"""
        # class:service -> method:status can store in cache
        cobj = Cache()
        cobj.set(current_app.config['LAST_MODI_KEY'], time())
        sobj = Service()
        self.assertNotEqual(sobj.status(), None)
        cobj.delete(current_app.config['LAST_MODI_KEY'])

        # class:service -> method:status can have value when cache deleted
        self.assertEqual(sobj.status(), None)

    def test_method_get_from_server(self):
        """--> class:service -> method:get_from_server 6 condition """
        sobj = Service()
        response = sobj.get_from_server()
        self.assertNotEqual(response, None)
        self.assertGreater(len(response), 1)
        self.assertEqual(type(response), list)
        self.assertIsInstance(len(response), object)

        element = response.pop().keys()
        keys = ['id', 'title', 'director', 'producer', 'release_date', 'rt_score', 'people']
        self.assertListEqual(list(element), keys)
        self.assertGreater(len(element), 1)

    def test_method_get_from_cache(self):
        """--> class:service -> method:getFromCache 6 condition """
        sobj = Service()
        data = sobj.get_from_server()
        cobj = Cache()
        cobj.set(current_app.config['LIST_DATA_KEY'], data)
        response = sobj.get_from_cache()
        self.assertNotEqual(response, None)
        self.assertGreater(len(response), 1)
        self.assertEqual(type(response), list)
        self.assertIsInstance(len(response), object)

        element = response.pop().keys()
        keys = ['id', 'title', 'director', 'producer', 'release_date', 'rt_score', 'people']
        self.assertListEqual(list(element), keys)
        self.assertGreater(len(element), 1)
        cobj.delete(current_app.config['LAST_MODI_KEY'])
        cobj.delete(current_app.config['LIST_FILM_KEY'])
        cobj.delete(current_app.config['LIST_DATA_KEY'])

        # class:service -> method:status can have value when cache deleted
        self.assertEqual(sobj.status(), None)

    def test_method_get_from_server_cache(self):

        """--> class:service -> method:get_from_server 12 condition """
        cobj = Cache()
        sobj = Service()
        cobj.delete(current_app.config['LAST_MODI_KEY'])
        cobj.delete(current_app.config['LIST_FILM_KEY'])
        cobj.delete(current_app.config['LIST_DATA_KEY'])
        self.assertEqual(cobj.get(current_app.config['LAST_MODI_KEY']), None)
        self.assertEqual(cobj.get(current_app.config['LIST_FILM_KEY']), None)
        self.assertEqual(cobj.get(current_app.config['LIST_DATA_KEY']), None)

        self.assertEqual(sobj.status(), None)
        sobj.get_from_server()
        self.assertNotEqual(sobj.status(), None)
        self.assertNotEqual(cobj.get(current_app.config['LAST_MODI_KEY']), None)
        self.assertNotEqual(cobj.get(current_app.config['LIST_FILM_KEY']), None)
        self.assertNotEqual(cobj.get(current_app.config['LIST_DATA_KEY']), None)

        cobj.delete(current_app.config['LAST_MODI_KEY'])
        cobj.delete(current_app.config['LIST_FILM_KEY'])
        cobj.delete(current_app.config['LIST_DATA_KEY'])
        self.assertEqual(sobj.status(), None)
        self.assertEqual(cobj.get(current_app.config['LAST_MODI_KEY']), None)
        self.assertEqual(cobj.get(current_app.config['LIST_FILM_KEY']), None)
        self.assertEqual(cobj.get(current_app.config['LIST_DATA_KEY']), None)

    def test_method_get_cache_update(self):
        """--> class:service -> method:get_cache_update 7 condition """

        # 1. Clear all cache
        cobj = Cache()
        cobj.delete(current_app.config['LAST_MODI_KEY'])
        cobj.delete(current_app.config['LIST_FILM_KEY'])
        cobj.delete(current_app.config['LIST_DATA_KEY'])
        # 2. create data on cache
        obj = Service()
        data = obj.get_from_server()
        # 3. Check cache
        total_before = {}
        total_before['data_on_cache'] = len(data)
        # 4. Test cache status
        self.assertNotEqual(obj.status(), None)
        self.assertNotEqual(cobj.get(current_app.config['LAST_MODI_KEY']), None)
        self.assertNotEqual(cobj.get(current_app.config['LIST_FILM_KEY']), None)
        self.assertNotEqual(cobj.get(current_app.config['LIST_DATA_KEY']), None)

        # 5. Removing one element from cache list
        list_in_cache = cobj.get(current_app.config['LIST_FILM_KEY'])
        total_before['list_on_cache'] = len(list_in_cache)
        list_in_cache.pop()
        cobj.set(current_app.config['LIST_FILM_KEY'], list_in_cache)
        list_in_cache = cobj.get(current_app.config['LIST_FILM_KEY'])
        self.assertEqual((total_before['list_on_cache'] - 1), len(list_in_cache))

        # 6. Update the cache
        obj = Service()
        obj.get_cache_update()
        sleep(2)
        # 7 Check data increase by 1
        self.assertEqual((total_before['data_on_cache'] + 1),
                         len(cobj.get(current_app.config['LIST_DATA_KEY'])))

        cobj.delete(current_app.config['LAST_MODI_KEY'])
        cobj.delete(current_app.config['LIST_FILM_KEY'])
        cobj.delete(current_app.config['LIST_DATA_KEY'])

        # class:service -> method:status can have value when cache deleted
        self.assertEqual(obj.status(), None)


if __name__ == '__main__':
    unittest.main()
