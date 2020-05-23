import collections
from re import split
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
    # Parameter id
    # Requirement: id(film id)
    # Return dict
    # Description: get the detail of single film
    # /
    def singleFilm(self, id):
        return json.loads(urlopen('{}/{}/{}'.format(self.api_url, 'films', id)).read())

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
    # Parameter id
    # Return object of people class
    # /
    def people(self, id=None):
        if id is None:
            return people(self.get())
        else:
            self.film = self.singleFilm(id)
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
        self.all_people = self.people()
        self.group_by_film = collections.defaultdict(list)

    # /
    # Get dict
    # parameter: None
    # Requirement: collections.defaultdict(list)
    # Return: self.group_by_film
    # Description: it group the people film to reduce number of iteration
    # /
    def group(self):
        for x in self.people():
            self.filter(x)
        return self.group_by_film

    # /
    # Method: Internal function
    # Return: clean data
    # Description: It will remove url attached in dict data['films'] which used to pair film with people
    # /
    def filter(self, data):
        data_copy = data.copy()
        data_copy.pop('films')
        for film in data['films']:
            self.group_by_film[film.replace('{}/{}/'.format(self.api_url, 'films'), '')].append(data_copy)

    # /
    # Get film detail with people
    # Parameter None
    # Return: dict
    # Description: Extend film detail with people
    # /
    def bind(self, data):
        # get all people of movie
        self.film['people'] = data
        return self.film

    # /
    # Not in use
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
    # not in use
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
        self.people_group = dict(people().group())
        # self.films_list = [1, 2, 3, 4, 5]

    # /
    # Get list
    # Requirement: self.films_list object of films list
    # Return: list of film id in list form
    # /
    def film_ids(self):
        return [list['id'] for list in self.films_list]

    def getSingle(self, film_id):
        if film_id in self.people_group:
            return movie().people(film_id).bind(self.people_group[film_id])
        else:
            return movie().people(film_id).bind({})

    # /
    # Get list
    # Parameter list(list)
    # Requirement list(param) will be null
    # Return: list of all films with there people associated
    # Description: Its a recursive function
    # /
    def get(self, list=[]):
        if len(self.films_list) > 0:
            pop_movie = self.films_list.pop()
            if pop_movie['id'] in self.people_group:
                list.append(movie(pop_movie).people().bind(self.people_group[pop_movie['id']]))
            else:
                list.append(movie(pop_movie).people().bind({}))
            self.get(list)
        return list