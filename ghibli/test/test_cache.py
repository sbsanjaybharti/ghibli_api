#!/usr/bin/env python3
"""
Import packages
"""
import unittest

from base import BaseTestCase, existsin
from src.service import Cache

class TestCacheMethodExist(BaseTestCase):
    """Test the class exist status"""

    @existsin(Cache)
    def test_class_have_method_get(self):
        """--> class:cache -> method:get exists"""

    @existsin(Cache)
    def test_class_have_method_set(self):
        """--> class:cache -> method:get exists"""

    @existsin(Cache)
    def test_class_have_method_delete(self):
        """--> class:cache -> method:delete exists"""

class TestCacheMethods(BaseTestCase):
    """Test class methods"""

    def test_method_set(self):
        """--> class:cache -> method:set store in cache """
        obj = Cache()
        request_key = 'some_key'
        request_data = 'test_data'
        self.assertNotEqual(obj.set(request_key, request_data), None)
        self.assertEqual(obj.set(request_key, request_data), 'test_data')

    def test_method_get(self):
        """--> class:cache -> method:get get from cache """
        obj = Cache()
        request_key = 'some_key'
        request_data = {'a': 'b', 'c': 'd'}
        obj.set(request_key, request_data)
        self.assertNotEqual(obj.get(request_key), None)
        self.assertEqual(obj.get(request_key), {'a': 'b', 'c': 'd'})

    def test_method_delete(self):
        """--> class:cache -> method:delete delete key """
        obj = Cache()
        request_key = 'some_key'
        request_data = {'a': 'b', 'c': 'd'}
        obj.set(request_key, request_data)
        self.assertNotEqual(obj.get(request_key), None)
        self.assertEqual(obj.get(request_key), {'a': 'b', 'c': 'd'})
        obj.delete(request_key)
        self.assertEqual(obj.get(request_key), None)


if __name__ == '__main__':
    unittest.main()
