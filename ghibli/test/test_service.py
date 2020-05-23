import unittest

from flask import Flask, current_app
from base import BaseTestCase, existsin
from src.service import service, cache
from time import time, sleep
from flask import Flask

class TestServiceMethodExist(BaseTestCase):

    @existsin(service)
    def test_class_have_method_status(self):
        """--> class:service -> method:status exists"""

    @existsin(service)
    def test_class_have_method_getFromServer(self):
        """--> class:service -> method:getFromServer exists"""

    @existsin(service)
    def test_class_have_method_getFromCache(self):
        """--> class:service -> method:getFromCache exists"""

    @existsin(service)
    def test_class_have_method_getCacheUpdate(self):
        """--> class:service -> method:getCacheUpdate exists"""

class TestServiceMethods(BaseTestCase):

    def cache(self):
        return cache()

    def service(self):
        return service()

    # class to test status function
    def test_method_status_null(self):
        """--> class:service -> method:status value can be null"""
        obj = service()
        self.assertEqual(self.service().status(), None)

    def test_method_status_not_null(self):
        """--> class:service -> method:status can have value"""
        """--> class:service -> method:status can store in cache"""
        # self.cache = cache()
        self.cache().set(current_app.config['LAST_MODI_KEY'], time())

        obj = service()
        self.assertNotEqual(self.service().status(), None)
        self.cache().delete(current_app.config['LAST_MODI_KEY'])
        """
        --> class:service -> method:status can have value when cache deleted
        """
        self.assertEqual(self.service().status(), None)

    def test_method_getFromServer(self):
        """--> class:service -> method:getFromServer 6 condition """
        obj = service()
        response = self.service().getFromServer()
        self.assertNotEqual(response, None)
        self.assertGreater(len(response), 1)
        self.assertEqual(type(response), list)
        self.assertIsInstance(len(response), object)

        element = response.pop().keys()
        keys = ['id', 'title', 'director', 'producer', 'release_date', 'rt_score', 'people']
        self.assertListEqual(list(element), keys)
        self.assertGreater(len(element), 1)

    def test_method_getFromCache(self):
        """--> class:service -> method:getFromCache 6 condition """
        obj = service()
        data = self.service().getFromServer()
        # cobj = cache()
        self.cache().set(current_app.config['LIST_DATA_KEY'], data)
        response = self.service().getFromCache()
        self.assertNotEqual(response, None)
        self.assertGreater(len(response), 1)
        self.assertEqual(type(response), list)
        self.assertIsInstance(len(response), object)

        element = response.pop().keys()
        keys = ['id', 'title', 'director', 'producer', 'release_date', 'rt_score', 'people']
        self.assertListEqual(list(element), keys)
        self.assertGreater(len(element), 1)
        self.cache().delete(current_app.config['LAST_MODI_KEY'])
        self.cache().delete(current_app.config['LIST_FILM_KEY'])
        self.cache().delete(current_app.config['LIST_DATA_KEY'])
        """
        --> class:service -> method:status can have value when cache deleted
        """
        self.assertEqual(self.service().status(), None)

    def test_method_getFromServer_Cache(self):
        """--> class:service -> method:getFromServer 12 condition """
        # cobj = cache()
        self.cache().delete(current_app.config['LAST_MODI_KEY'])
        self.cache().delete(current_app.config['LIST_FILM_KEY'])
        self.cache().delete(current_app.config['LIST_DATA_KEY'])
        self.assertEqual(self.cache().get(current_app.config['LAST_MODI_KEY']), None)
        self.assertEqual(self.cache().get(current_app.config['LIST_FILM_KEY']), None)
        self.assertEqual(self.cache().get(current_app.config['LIST_DATA_KEY']), None)
        obj = service()
        self.assertEqual(self.service().status(), None)
        self.service().getFromServer()
        self.assertNotEqual(self.service().status(), None)
        self.assertNotEqual(self.cache().get(current_app.config['LAST_MODI_KEY']), None)
        self.assertNotEqual(self.cache().get(current_app.config['LIST_FILM_KEY']), None)
        self.assertNotEqual(self.cache().get(current_app.config['LIST_DATA_KEY']), None)

        self.cache().delete(current_app.config['LAST_MODI_KEY'])
        self.cache().delete(current_app.config['LIST_FILM_KEY'])
        self.cache().delete(current_app.config['LIST_DATA_KEY'])
        self.assertEqual(self.service().status(), None)
        self.assertEqual(self.cache().get(current_app.config['LAST_MODI_KEY']), None)
        self.assertEqual(self.cache().get(current_app.config['LIST_FILM_KEY']), None)
        self.assertEqual(self.cache().get(current_app.config['LIST_DATA_KEY']), None)

    def test_method_getCacheUpdate(self):
        """--> class:service -> method:getCacheUpdate 7 condition """

        # 1. Clear all cache
        cobj = cache()
        self.cache().delete(current_app.config['LAST_MODI_KEY'])
        self.cache().delete(current_app.config['LIST_FILM_KEY'])
        self.cache().delete(current_app.config['LIST_DATA_KEY'])
        # 2. create data on cache
        obj = service()
        data = obj.getFromServer()
        # 3. Check cache
        total_before={}
        total_before['data_on_cache'] = len(data)
        # 4. Test cache status
        self.assertNotEqual(obj.status(), None)
        self.assertNotEqual(self.cache().get(current_app.config['LAST_MODI_KEY']), None)
        self.assertNotEqual(self.cache().get(current_app.config['LIST_FILM_KEY']), None)
        self.assertNotEqual(self.cache().get(current_app.config['LIST_DATA_KEY']), None)

        # 5. Removing one element from cache list
        list_in_cache = self.cache().get(current_app.config['LIST_FILM_KEY'])
        total_before['list_on_cache'] = len(list_in_cache)
        pop = list_in_cache.pop()
        self.cache().set(current_app.config['LIST_FILM_KEY'], list_in_cache)
        list_in_cache = self.cache().get(current_app.config['LIST_FILM_KEY'])
        self.assertEqual((total_before['list_on_cache']-1), len(list_in_cache))

        # 6. Update the cache
        obj = service()
        data = obj.getCacheUpdate()
        sleep(2)
        # 7 Check data increase by 1
        self.assertEqual((total_before['data_on_cache'] + 1), len(self.cache().get(current_app.config['LIST_DATA_KEY'])))

        self.cache().delete(current_app.config['LAST_MODI_KEY'])
        self.cache().delete(current_app.config['LIST_FILM_KEY'])
        self.cache().delete(current_app.config['LIST_DATA_KEY'])
        """
        --> class:service -> method:status can have value when cache deleted
        """
        self.assertEqual(obj.status(), None)

if __name__ == '__main__':
    unittest.main()