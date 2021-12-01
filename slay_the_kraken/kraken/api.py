#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hmac
import json
import requests

from time import time_ns
from hashlib import sha256, sha512
from urllib.parse import urlencode
from base64 import b64encode, b64decode

from slay_the_kraken.kraken.exceptions import KrakenError


class API(object):
    """Represents an instance that communicates with the kraken exchange."""
    # Private:
    _api_key: str = ''
    _api_secret: str = ''
    _api_version: str = '0'
    _timeout: float = 5.0
    _json_options: dict = {}

    # Public:
    api_url: str = 'https://api.kraken.com'
    session: requests.Session = requests.Session()
    respons: requests.Response = requests.Response()

    def __init__(self) -> None:
        self._load_keys()

    def _load_keys(self) -> None:
        """Load keys from the .env directory into memory."""
        with open('slay_the_kraken/env/api_keys.json', 'r') as myfile:
            api_keys_data = json.load(myfile)
        self._api_key: str = api_keys_data['KRAKEN_API_KEY']
        self._api_secret: str = api_keys_data['KRAKEN_API_SECRET']

    def _nonce(self) -> int:
        """An ever increasing value as unique identifier."""
        return int(time_ns())

    def _query(self, url: str, headers: dict, data: dict, timeout: float) -> dict:
        """Wrapper around a simple request."""
        url: str = self.api_url + url
        self.response = self.session.post(url, headers=headers, data=data, timeout=timeout)
        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()
        response_json = self.response.json(**self._json_options)
        kraken_api_error = response_json['error']
        if kraken_api_error:
            raise KrakenError(kraken_api_error)
        return response_json

    def _signature(self, url_path: str, data: dict) -> str:
        """Sign and hash the given data."""
        nonce = str(data['nonce'])
        data_encoded = urlencode(data)
        # Unicode-objects must be encoded before hashing
        encoded = (nonce + data_encoded).encode()
        message = url_path.encode() + sha256(encoded).digest()
        signature = hmac.new(b64decode(self._api_secret), message, sha512)
        sigdigest = b64encode(signature.digest())
        return sigdigest.decode()

    def close(self):
        """Close the connection to the exchange."""
        self.session.close()

    def public_query(self, method: str, data: dict) -> dict:
        """Query without having to sign."""
        url: str = '/' + self._api_version + '/public/' + method
        return self._query(url, headers={}, data=data, timeout=self._timeout)

    def private_query(self, method: str, data: dict) -> dict:
        """Query with having to sign."""
        url: str = '/' + self._api_version + '/private/' + method
        data['nonce'] = self._nonce()
        headers: dict = {'API-Key': self._api_key, 'API-Sign': self._signature(url, data)}
        return self._query(url, headers=headers, data=data, timeout=self._timeout)

    def Balance(self) -> dict:
        """Returns the account balance."""
        result: dict = self.private_query('Balance', data={})
        return result

    def OHLC(self, pair: str, interval: int = 5) -> dict:
        """Return the open-high-low-close data for a given asset."""
        intervals: list[int] = [1, 5, 15, 30, 60, 4*60, 24*60, 7*24*60, 15*24*60]  # in minutes
        if interval not in intervals:
            interval = 1
        return self.public_query('OHLC', data={'pair': pair, 'interval': interval})
