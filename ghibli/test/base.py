from flask_testing import TestCase
from functools import wraps
from src.config import create_app
from src.service import cache

#############################################################################
# Class for basic setup for testing which can be use as a base class
#############################################################################
class BaseTestCase(TestCase):
    """ Base Tests """
    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        cache_obj = cache()
        cache_obj.delete(self.create_app().config['LAST_MODI_KEY'])
        cache_obj.delete(self.create_app().config['LIST_FILM_KEY'])
        cache_obj.delete(self.create_app().config['LIST_DATA_KEY'])

def existsin(namespace):
    """Given a namespace, this decorator asserts that an object with
    the same name as the function it's wrapping (minus ) exists in that
    namespace"""
    def wrapper(namedunittest):
        assert namedunittest.__name__.startswith('test_class_have_method_'), \
            "The wrapped '%s' function doesn't look like a unit test" % namedunittest.__name__

        @wraps(namedunittest)
        def inner(self, *args, **kwargs):
            self.assertTrue(hasattr(namespace, namedunittest.__name__.split('_class_have_method_')[1]))
            return namedunittest(self, *args, **kwargs)
        return inner
    return wrapper