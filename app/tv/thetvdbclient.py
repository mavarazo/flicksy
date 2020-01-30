import requests

class Serie():

    def __init__(self, id, seriesName, banner=None, firstAired=None, image=None, overview=None, poster=None):
        self.banner = banner
        self.firstAired = firstAired
        self.id = id
        self.overview = overview
        self.poster = poster
        self.seriesName = seriesName

    def __str__(self):
        return f"{self.seriesName} ({self.id})"
        

class TheTvDbException(Exception):

    def __init__(self, status, message='Unkown error.', response=None):
        self.status = status
        self.message = message
        self.response = response

    def __str__(self):
        return f"{self.status} ({self.message})"

    def __repr__(self):
        f"{self.__class__.__name__} (status={self.status})"


class TheTvDbClient():
    BASE_URL = 'https://api.thetvdb.com'

    def __init__(self, apikey=None):
        self.token = None
        if apikey is not None:
            self.init_app(apikey, token)

    def init_app(self, apikey):
        self.apikey = apikey

    def login(self):
        response = requests.post(
            self.BASE_URL + '/login', json={"apikey": self.apikey})
        if response:
            self.token = response.json()['token']
        elif response.status_code == 401:
            raise TheTvDbException(response.status_code,
                                   'Invalid credentials and/or API token.')
        else:
            raise TheTvDbException(response.status_code)

    def search_series(self, name):
        params = {'name': name}
        headers = {'Authorization': 'Bearer %s' % self.token}
        response = requests.get(
            self.BASE_URL + '/search/series', params=params, headers=headers)
        if response:
            return response.json()
        elif response.status_code == 401:
            self.login()
            return self.search_series(name)
        elif response.status_code == 404:
            raise TheTvDbException(
                response.status_code, 'No records are found that match your query.')
        else:
            raise TheTvDbException(response.status_code)

    def search_episode(self, seriesId, seasonnumber, episodenumber):
        params = {'airedSeason': seasonnumber,
                  'airedEpisode': episodenumber}
        headers = {'Authorization': 'Bearer %s' % self.token}
        response = requests.get(f"{self.BASE_URL}/series/{seriesId}/episodes/query", params=params, headers=headers)
        if response:
            return response.json()
        elif response.status_code == 401:
            self.login()
            return self.search_series(name)
        elif response.status_code == 404:
            print(f"{seriesId}/{seasonnumber}/{episodenumber}")
            raise TheTvDbException(
                response.status_code, 'No records are found that match your query.')
        else:
            raise TheTvDbException(response.status_code)
