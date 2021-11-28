import unittest

from slay_the_kraken.kraken.api import API


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

    def test_signature(self) -> None:
        """Make a fake order and test whether the signature is as expected."""
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


if __name__ == '__main__':
    unittest.main()
