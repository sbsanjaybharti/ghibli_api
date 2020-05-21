from urllib.request import urlopen
from flask import current_app
import json

class ghibhi:

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
    # Return film list with detail of each film
    # /
    def films(self):
        return json.loads(urlopen('{}/{}'.format(self.api_url, 'films')).read())

    # /
    # Get Raw data
    # Parameter None
    # Return people list with detail of each person
    # /
    def people(self):
        return json.loads(urlopen('{}/{}/?fields={}'.format(self.api_url, 'people', ','.join(self.people_fields))).read())

# Derived class of ghibhi
class movie(ghibhi):

    # /
    # Get based class constructor
    # Parameter film object of film
    # /
    def __init__(self, film=None):
        super(movie,self).__init__()
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
        it contain disc with pre-define key in ghibhi class
        :return: dict
        """
        if self.film is None:
            return {}
        return {i: self.film[i] for i in self.film_fields}

    # /
    # builder pattern: Extending movie for getting people
    # Parameter None
    # Return object of people class
    # /
    def people(self):
        return people(self.get())

# Derived class of ghibhi
class people(ghibhi):

    # /
    # Get based class constructor
    # Parameter film object of film
    # Requirement film(param) can be null
    # /
    def __init__(self, film=None):
        super(people,self).__init__()
        self.film = film

    # /
    # Get film detail with people
    # Parameter None
    # Return: dict
    # Description: Extend film detail with people
    # /
    def bind(self):
        # get all people of movie
        self.film['people'] = self.getByfilmID(self.film['id'])
        return self.film

    # /
    # Get people
    # parameter id (Id of film)
    # Requirement: id
    # Return: list
    # Description: get the list of people based on film id
    # /
    def getByfilmID(self, id):
        """
        Get the people list based on film ID
        :return: list
        """
        all_people = self.people()
        people_list = []
        people_key = self.people_fields.copy()
        people_key.remove('films')
        for people in all_people:
            if '{}/films/{}'.format(self.api_url, id) in people['films']:
                people_list.append({i: people[i] for i in people_key})
        return people_list

    # /
    # Get people
    # parameter id (Id of people)
    # Requirement: id
    # Return: Not implemented
    # Description: pass
    # /
    def get(self, id):
        pass


# Derived class of ghibhi
class BindMoviePeople(ghibhi):

    # /
    # Get based class constructor
    # Parameter films_list
    # Description: Get raw film list
    # /
    def __init__(self):
        super(BindMoviePeople,self).__init__()
        self.films_list = self.films()
        # self.films_list = [1, 2, 3, 4, 5]

    # /
    # Get films
    # Parameter list(list)
    # Requirement list(param) will be null
    # Return: list
    # Description: Recursion Method to get all films
    # /
    def get(self, list=[]):
        if len(self.films_list) > 0:
            list.append(movie(self.films_list.pop()).people().bind())
            self.get(list)
        response_object = {
            'code': 200,
            'type': 'Success',
            'data': list
        }
        return response_object