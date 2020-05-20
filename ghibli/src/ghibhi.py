
class ghibhi:

    def __init__(self, api_url):
        self.api_url = api_url


class movie:

    def __init__(self, id):
        self.id = id

    def get(self):
        """
        Get the movie detail based on movie ID
        it contain disc with following key
        {
            "id": string,
            "title": string,
            "description": string,
            "director": string,
            "producer": string,
            "release_date": integer,
            "rt_score": integer,
        }
        :return:
        """
        pass

    def people(self):
        pass



class people:

    def __init__(self):
        pass

    def get(self):
        pass
