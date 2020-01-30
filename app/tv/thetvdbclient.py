import requests


class Serie():

    def __init__(self, id, seriesName, banner=None, firstAired=None, image=None, overview=None, poster=None):
        self._id = id
        self._seriesName = seriesName
        self._banner = banner
        self._firstAired = firstAired
        self._overview = overview
        self._poster = poster

    @property
    def id(self):
        return self._id

    @property
    def seriesName(self):
        return self._seriesName

    @property
    def banner(self):
        return self._banner

    @property
    def firstAired(self):
        return self._firstAired

    @property
    def overview(self):
        return self._overview

    @property
    def poster(self):
        return self._poster

    def __str__(self):
        return f"{self._seriesName} ({self._id})"


class Episode():

    def __init__(self, id, airedSeason, airedEpisodeNumber, episodeName=None, imdbId=None, overview=None):
        self._id = id
        self._airedSeason = airedSeason
        self._airedEpisodeNumber = airedEpisodeNumber
        self._episodeName = episodeName
        self._imdbId = imdbId
        self._overview = overview

    @property
    def id(self):
        return self._id

    @property
    def airedSeason(self):
        return self._airedSeason

    @property
    def airedEpisodeNumber(self):
        return self._airedEpisodeNumber

    @property
    def episodeName(self):
        return self._episodeName

    @property
    def imdbId(self):
        return self._imdbId

    @property
    def overview(self):
        return self._overview

    def __str__(self):
        return f"{self._episodeName} ({self._id})"


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
            result = []
            for data in response.json()['data']:
                result.append(Serie(data['id'], data['seriesName'], data.get('banner', None), data.get('firstAired', None),
                                    data.get('image', None), data.get('overview', None), data.get('poster', None)))
            return result
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
        response = requests.get(
            f"{self.BASE_URL}/series/{seriesId}/episodes/query", params=params, headers=headers)
        if response:
            result = []
            for data in response.json()['data']:
                result.append(Episode(data['id'], data['airedSeason'], data['airedEpisodeNumber'], data.get('episodeName', None),
                                      data.get('imdbId', None), data.get('overview', None)))
            return result
        elif response.status_code == 401:
            self.login()
            return self.search_series(name)
        elif response.status_code == 404:
            print(f"{seriesId}/{seasonnumber}/{episodenumber}")
            raise TheTvDbException(
                response.status_code, 'No records are found that match your query.')
        else:
            raise TheTvDbException(response.status_code)
