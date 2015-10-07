from unittest import TestCase
from unittest.mock import patch

import requests.exceptions

import infiksi
from tests import utils


class MockResponse(object):
    def __init__(self, status_code, text, url=None):
        self.url = url
        self.text = text
        self.status_code = status_code


class RetrieveHtmlTest(TestCase):
    def test_medievalbooksnl_posters(self):
        expected = utils._load_fixture("medievalbooksnl_posters.html")

        with patch('requests.get') as mock:
            mock.return_value = MockResponse(200, expected, url='http://medievalbooks.nl/2015/09/04/medieval-posters/')
            html, url = infiksi.retrieve_html("http://medievalbooks.nl/2015/09/04/medieval-posters/")

        self.assertEquals(html, expected)
        self.assertEquals(url, 'http://medievalbooks.nl/2015/09/04/medieval-posters/')

    def test_non_existing_domain(self):
        with patch('requests.get') as mock:
            mock.side_effect = requests.exceptions.ConnectTimeout()
            self.assertRaises(infiksi.UnreachableError, infiksi.retrieve_html, "http://does-not-exist.example.com")

    def test_server_error(self):
        with patch('requests.get') as mock:
            mock.return_value = MockResponse(500, '')
            self.assertRaises(infiksi.TemporaryError, infiksi.retrieve_html, '...')

    def test_page_does_not_exist(self):
        with patch('requests.get') as mock:
            mock.return_value = MockResponse(404, '')
            self.assertRaises(infiksi.UnreachableError, infiksi.retrieve_html, '...')

    def test_page_with_too_many_redirects(self):
        with patch('requests.get') as mock:
            mock.side_effect = requests.exceptions.TooManyRedirects()
            self.assertRaises(infiksi.UnreachableError, infiksi.retrieve_html, '...')

    def test_page_with_redirected_result(self):
        with patch('requests.get') as mock:
            mock.return_value = MockResponse(200, '', url='http://blah')
            html, url = infiksi.retrieve_html('...')

            self.assertEquals(url, 'http://blah')
