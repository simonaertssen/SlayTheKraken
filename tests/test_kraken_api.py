import time
import unittest

from unittest import mock
from time import gmtime, strftime

from slay_the_kraken.kraken.api import API
from slay_the_kraken.kraken.exceptions import KrakenError


class TestKrakenAPI(unittest.TestCase):
    """Test the kraken api."""

    def setUp(self) -> None:
        """Declare an instance of the api."""
        self.api: API = API()

    def test_construction(self) -> None:
        """Test whether the class was constructed correctly."""
        self.assertEqual(self.api._api_version, '0')
        self.assertEqual(self.api.api_url, 'https://api.kraken.com')
        self.assertNotEqual(self.api._api_key, str())
        self.assertNotEqual(self.api._api_secret, str())

    def test_nonce(self) -> None:
        """Test whether the nonce returns an increasing number."""
        first: int = self.api._nonce()
        secnd: int = self.api._nonce()
        self.assertLess(first, secnd)

    def test_errors(self) -> None:
        """Test whether the error/exception mechanism works correctly."""
        def minus(): return -1
        with mock.patch.object(self.api, '_nonce', minus):
            with self.assertRaises(KrakenError) as ne:
                self.api.Balance()
            self.assertEqual(str(ne.exception), "['EAPI:Invalid nonce']")

    def test_signature(self) -> None:
        """Make a fake order and test whether the signature is as expected."""
        tmp: str = self.api._api_secret
        self.api._api_secret = 'kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg=='
        url: str = '/0/private/AddOrder'
        data: dict = {
            'nonce': '1616492376594',
            'ordertype': 'limit',
            'pair': 'XBTUSD',
            'price': 37500,
            'type': 'buy',
            'volume': 1.25
        }

        expected: str = '4/dpxb3iT4tp/ZCVEwSnEsLxx0bqyhLpdfOpc6fn7OR8+UClSV5n9E6aSS8MPtnRfp32bAb0nmbRn6H8ndwLUQ=='
        received: str = self.api._signature(url, data)
        self.assertEqual(received, expected)
        self.api._api_secret = tmp

    def test_public_method(self) -> None:
        """Test whether the public requests function correctly."""
        unixtime: int = int(time.time())

        servertime: dict = self.api.public_query('Time', data={})
        self.assertEqual(servertime['error'], [])
        self.assertAlmostEqual(servertime['result']['unixtime'], unixtime, -1)

        rfc1123: str = strftime("%a, %d %b %y %H:%M:%S +0000", gmtime())
        self.assertEqual(servertime['result']['rfc1123'], rfc1123)

    def test_private_method(self) -> None:
        """Test whether the private requests function correctly."""
        balance: dict = self.api.Balance()
        self.assertEqual(balance['error'], [])
        self.assertIsInstance(balance['result'], dict)

    def test_api(self):
        # print(self.api.OHLC('ZEUR', ))
        # self.api.OHLC('ZEUR', interval=1)
        # self.api.OHLC('ZEUR', since=time() - )
        # self.api.OHLC('ZEUR', interval=1)
        print(self.api.OHLC('ZEUR', interval=1))


if __name__ == '__main__':
    unittest.main()
