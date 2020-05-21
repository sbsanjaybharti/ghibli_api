from flask_testing import TestCase
from flask import Flask
from src.config import create_app

#############################################################################
# Class for basic setup for testing which can be use as a base class
#############################################################################
class BaseTestCase(TestCase):
    """ Base Tests """
    def create_app(self):
        app = create_app('testing')
        return app
