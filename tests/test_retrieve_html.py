from unittest import TestCase
from unittest.mock import patch
import requests.exceptions

import infiksi
from tests import utils


class MockResponse(object):
    def __init__(self, status_code, text):
        self.text = text
        self.status_code = status_code


class RetrieveHtmlTest(TestCase):

    def test_medievalbooksnl_posters(self):
        expected = utils._load_fixture("medievalbooksnl_posters.html")

        with patch('requests.get') as mock:
            mock.return_value = MockResponse(200, expected)
            html = infiksi.retrieve_html("http://medievalbooks.nl/2015/09/04/medieval-posters/")

        self.assertEquals(html, expected)

    def test_non_existing_domain(self):

        with patch('requests.get') as mock:
            mock.side_effect = requests.exceptions.ConnectTimeout()
            self.assertRaises(infiksi.UnreachableError, infiksi.retrieve_html, "http://does-not-exist.example.com")
