import time
import hmac
import json
import requests

from typing import Dict
from urllib.parse import urlencode
from hashlib import sha256, sha512
from base64 import b64encode, b64decode


class API(object):
    # Private:
    _api_key: str     = ""
    _api_secret: str  = ""
    _api_version: str = '0'
    _timeout: float   = 1.0

    # Public:
    api_url: str = 'https://api.kraken.com'
    session: requests.Session  = requests.Session()
    respons: requests.Response = requests.Response()

    def __init__(self) -> None:
        self._load_keys()

    def _load_keys(self) -> None:
        with open('../env/api_keys.json', 'r') as myfile:
            api_keys_data = json.load(myfile)
        self._api_key = api_keys_data['KRAKEN_API_KEY']
        self._api_secret = api_keys_data['KRAKEN_API_SECRET']

    def _nonce(self) -> int:
        return int(time.time())

    def _query(self, url: str, headers: dict, data: dict, timeout: float) -> dict:
        url = self.api_url + url
        self.response = self.session.post(url, headers=headers, data=data, timeout=timeout)
        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()
        return self.response.json()

    def _signature(self, url_path: str, data: dict) -> str:
        nonce = str(data['nonce'])
        data_encoded = urlencode(data)

        # Unicode-objects must be encoded before hashing
        encoded = (nonce + data_encoded).encode()
        message = url_path.encode() + sha256(encoded).digest()
        signature = hmac.new(b64decode(self._api_secret), message, sha512)
        sigdigest = b64encode(signature.digest())
        return sigdigest.decode()

    def public_query(self, method: str, data: dict, timeout: int) -> dict:
        url = '/' + self._api_version + '/public/' + method
        return self._query(url, headers={}, data=data, timeout=timeout)

    def private_query(self, method: str, data: dict, timeout: int) -> dict:
        url = '/' + self._api_version + '/private/' + method
        data['nonce'] = self._nonce()
        headers = {'API-Key': self._api_key, 'API-Sign': self._signature(url, data)}
        return self._query(url, headers=headers, data=data, timeout=timeout)
    
    def Balance(self) -> float:
        result = self.private_query('Balance', data={}, timeout=self._timeout)
        return result

    def OpenPositions(self) -> float:
        result = self.private_query('OpenPositions', data={}, timeout=self._timeout)
        return result

    # def TradeBalance(self) -> float:
    #     data = {}
    #     result = self.private_query('TradeBalance', data={}, timeout=self._timeout)
    #     print(result)
    #     return result


if __name__ == '__main__':
    krakenapi = API()
    b = krakenapi.private_query('QueryLedgers', data={'id': [0, 1]}, timeout=1.0)
    print(b)