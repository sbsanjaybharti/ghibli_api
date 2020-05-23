import json
from time import time

from flask import current_app
from pymemcache.client.base import Client
from .ghibhi import BindMoviePeople

class JsonSerde(object):
    """Serialize and deserialize data to store in cache"""

    def serialize(self, key, value):
        if isinstance(value, str):
            return value, 1
        return json.dumps(value), 2

    def deserialize(self, key, value, flags):
       if flags == 1:
           return value
       if flags == 2:
           return json.loads(value)
       raise Exception("Unknown serialization format")

class cache:

    """Base class of cache"""
    # /
    # Get access to cache server
    # variable: ENV variable required CACHE_SERVER and CACHE_PORT
    # Requirement: hostname, port
    # Return: setting return permission to read and wright on memcache server
    # /
    def __init__(self):
        self.client = Client((current_app.config['CACHE_SERVER'], int(current_app.config['CACHE_PORT'])), serde=JsonSerde())

    # /
    # Set write in cache
    # parameter key, data
    # Requirement: key, data
    # Return: data
    # Description: write data with key pair
    # /
    def set(self, key, data):
        self.client.set(key, data)
        return data

    # /
    # Get read data
    # parameter key
    # Requirement: key
    # Return: data
    # Description: read the data of specific key pair
    # /
    def get(self, key):
        return self.client.get(key)

    # /
    # parameter key
    # Return: None
    # Description: used to delete key from cache server
    # /
    def delete(self, key):
        return self.client.delete(key)

class service:
    """Class connect cache class with data processing classes"""
    # /
    # variable: last_modification_key, movie_list_key, movie_data_key
    # Requirement: pre define
    # Description: Pre define variable to have consistency
    # /
    def __init__(self):
        self.last_modification_key = current_app.config['LAST_MODI_KEY']
        self.movie_list_key = current_app.config['LIST_FILM_KEY']
        self.movie_data_key = current_app.config['LIST_DATA_KEY']
        self.cache = cache()

    # /
    # Get time
    # parameter: None
    # Requirement: last_modification_key
    # Return: None or last update time from now
    # Description: Used to check how old is cache
    # /
    def status(self):

        now = time()
        if self.cache.get(self.last_modification_key) is None:
            return None
        else:
            return (now - self.cache.get(self.last_modification_key))

    # /
    # Get data
    # parameter: None
    # Requirement: ghibhi access class required
    # Return: data
    # Description: It will get the data from main server ad update cache used in initial stage
    # /
    def getFromServer(self):
        """Get from main server"""
        data = BindMoviePeople().get()
        """Set data cache"""
        self.cache.set(self.movie_data_key, data)
        """Set cache creation time"""
        self.cache.set(self.last_modification_key, time())
        """Set cache list of movie id"""
        self.cache.set(self.movie_list_key, [sub['id'] for sub in data])
        # print(data.keys())
        return data

    # /
    # Get data
    # parameter: None
    # Requirement: movie_data_key
    # Return: data
    # Description: if cache is not older than 1 min then get the data from cache
    # /
    def getFromCache(self):
        return self.cache.get(self.movie_data_key)

    # /
    # Get data
    # parameter: None
    # Requirement: movie_list_key, movie_data_key
    # Return: data
    # Description: if cache is older than check new release and append in current cache
    # /
    def getCacheUpdate(self):

        """
        Compare the list from api with list from cache
        and get the list which is not in cache
        """
        cache_data_keys = self.cache.get(self.movie_list_key)
        server_data_keys = BindMoviePeople().film_ids()
        data = self.cache.get(self.movie_data_key)
        for record in list(set(server_data_keys) - set(cache_data_keys)):
            data.append(BindMoviePeople().getSingle(record))

        """Set data cache"""
        self.cache.set(self.movie_data_key, data)
        """Set cache creation time"""
        self.cache.set(self.last_modification_key, time())
        """Set cache list of movie id"""
        self.cache.set(self.movie_list_key, [sub['id'] for sub in data])
        # print(data.keys())
        return data
