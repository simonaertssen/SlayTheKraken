import requests

class API(object):

    # Private:
    _nonce_value = 0

    # Public:
    url = 'https://api.kraken.com'
    session = requests.Session()
    def __init__(self):
        
        pass

    def _nonce(self):
        self._nonce_value += 1
        return self._nonce_value

    def _query(self, url: str = "", header: dict = {}, data: dict = {}, timeout: float = 1.0):

        pass
