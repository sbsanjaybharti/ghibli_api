#!/usr/bin/env python3
"""
Import packages
"""
import collections
from urllib.request import urlopen
import json
from flask import current_app


class Ghibhi:
    """
    Class handle Ghibhi api
    """
    # /
    # Set Base class
    # Parameter None
    # class variable:
    #   api_url(string): get from ENV
    #   film_fields(list): fix the keys of field required
    #   people_fields(list): fix the keys for people fields
    # /
    def __init__(self):
        self.api_url = current_app.config['GHIBLI_API']
        self.film_fields = ['id', 'title', 'director', 'producer', 'release_date', 'rt_score']
        self.people_fields = ['id', 'name', 'gender', 'age', 'eye_color', 'hair_color', 'films']

    # /
    # Get Raw data
    # Parameter None
    # /
    def films(self):
        """
        Return film list with detail of each film
        """
        return json.loads(urlopen('{}/{}'.format(self.api_url, 'films')).read())

    # /
    # Get Raw data
    # Parameter id
    # Requirement: id(film id)
    # Return dict
    # /
    def single_film(self, film_id):
        """
        Description: get the detail of single film
        """
        return json.loads(urlopen('{}/{}/{}'.format(self.api_url, 'films', film_id)).read())

    # /
    # Get Raw data
    # Parameter None
    # Return people list with detail of each person
    # /
    def peoples(self):
        """
        Description: Format the keys
        """
        return json.loads(
            urlopen('{}/{}/?fields={}'.format(
                self.api_url,
                'people',
                ','.join(self.people_fields))\
            ).read())


# Derived class of Ghibhi
class Movie(Ghibhi):
    """
    Class handle films of Ghibhi api
    """

    # /
    # Get based class constructor
    # Parameter film object of film
    # /
    def __init__(self, film=None):
        super(Movie, self).__init__()
        self.film = film

    # /
    # Get data
    # Parameter None
    # Return: dict
    # Return detail of film based on fields as mention in based class
    # /
    def get(self):
        """
        Get the movie detail based on movie ID
        it contain disc with pre-define key in Ghibhi class
        :return: dict
        """
        if self.film is None:
            return {}
        return {i: self.film[i] for i in self.film_fields}

    # /
    # builder pattern: Extending movie for getting People
    # Parameter id
    # Return object of People class
    # /
    def people(self, film_id=None):
        """
        Description: Return Class:people object
        """
        if film_id is None:
            return People(self.get())
        self.film = self.single_film(film_id)
        return People(self.get())


# Derived class of Ghibhi
class People(Ghibhi):
    """
    Class handle people of Ghibhi api
    """
    # /
    # Get based class constructor
    # Parameter film object of film
    # Requirement film(param) can be null
    # /
    def __init__(self, film=None):
        super(People, self).__init__()
        self.film = film
        self.all_people = self.peoples()
        self.group_by_film = collections.defaultdict(list)

    # /
    # Get dict
    # parameter: None
    # Requirement: collections.defaultdict(list)
    # Return: self.group_by_film
    # /
    def group(self):
        """
        Description: it group the people film to reduce number of iteration
        """
        for row in self.peoples():
            self.filter(row)
        return self.group_by_film

    # /
    # Method: Internal function
    # Return: clean data
    # /
    def filter(self, data):
        """
        It will remove url attached in dict data['films'] which used to pair film with people
        """
        data_copy = data.copy()
        data_copy.pop('films')
        for film in data['films']:
            self.group_by_film[
                film.replace('{}/{}/'.format(self.api_url, 'films'), '')
            ].append(data_copy)

    # /
    # Get film detail with people
    # Parameter None
    # Return: dict
    # /
    def bind(self, data):
        """
        Extend film detail with people
        """
        # get all people of movie
        self.film['people'] = data
        return self.film
    #
    # # /
    # # Not in use
    # # /
    # def get_by_film_id(self, id):
    #     """
    #     Get the people list based on film ID
    #     :return: list
    #     """
    #     all_people = self.people()
    #     people_list = []
    #     people_key = self.people_fields.copy()
    #     people_key.remove('films')
    #
    #     for people in all_people:
    #         if '{}/films/{}'.format(self.api_url, id) in people['films']:
    #             people_list.append({i: people[i] for i in people_key})
    #     return people_list
    #
    # # /
    # # not in use
    # # /
    # def get(self, id):
    #     pass


# Derived class of Ghibhi
class BindMoviePeople(Ghibhi):
    """
    Class Adapter between class movie and People
    """
    # /
    # Get based class constructor
    # Parameter films_list
    # Description: Get raw film list
    # /
    def __init__(self):
        super(BindMoviePeople, self).__init__()
        self.films_list = self.films()
        self.people_group = dict(People().group())
        # self.films_list = [1, 2, 3, 4, 5]

    # /
    # Get list
    # Requirement: self.films_list object of films list
    # Return: list of film id in list form
    # /
    def film_ids(self):
        """
        List of all films id
        """
        return [list['id'] for list in self.films_list]

    # /
    # Get dict
    # Parameter: film_id
    # Requirement: film_id
    # Return: list of film id in list form
    # /
    def get_single(self, film_id):
        """
        Get detail of single film
        """
        if film_id in self.people_group:
            return Movie().people(film_id).bind(self.people_group[film_id])
        return Movie().people(film_id).bind({})

    # /
    # Get list
    # Parameter list(list)
    # Requirement list(param) will be null
    # Return: list of all films with there people associated
    # Description: Its a recursive function
    # /
    def get(self, lists=[]):
        """
        Get detail of single film in each iteration and push in list
        """
        if len(self.films_list) > 0:
            pop_movie = self.films_list.pop()
            if pop_movie['id'] in self.people_group:
                lists.append(Movie(pop_movie).people().bind(self.people_group[pop_movie['id']]))
            else:
                lists.append(Movie(pop_movie).people().bind({}))
            self.get(lists)
        return lists
