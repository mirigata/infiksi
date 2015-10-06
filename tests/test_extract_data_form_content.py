from unittest import TestCase
import os.path

import infiksi


def _load_fixture(fixture):
    with open(os.path.join(os.path.dirname(__file__), "fixtures", fixture)) as f:
        return f.read()


class ContentExtractionTest(TestCase):
    def test_extract_empty_html(self):
        result = infiksi.parse_contents(_load_fixture("empty.html"))
        self.assertIsNotNone(result)

        self.assertEquals(result.version, '1.0')
        self.assertEquals(result.type, 'article')

    def test_extract_from_title(self):
        result = infiksi.parse_contents(_load_fixture("beautifulpage.html"))
        self.assertIsNotNone(result)
        self.assertEquals(result.title, 'My Beautiful Page')

    def test_extract_from_livecodingtv(self):
        result = infiksi.parse_contents(_load_fixture("livecodingtv_publysher.html"))
        self.assertIsNotNone(result)

        self.assertEquals(result.title, 'Python: retrieving metadata from websites')
        self.assertEquals(result.description, '')
        self.assertEquals(result.og_title, 'watch people code products live')
        self.assertEquals(result.og_description, 'Python: retrieving metadata from websites')

    def test_extract_from_php_fractal(self):
        result = infiksi.parse_contents(_load_fixture("php_fractal_bad_design.html"))
        self.assertIsNotNone(result)
        self.assertEquals(result.title, 'PHP: a fractal of bad design / fuzzy notepad')
        self.assertEquals(result.author_name, 'Eevee')

    def test_extract_from_medievalbooks(self):
        result = infiksi.parse_contents(_load_fixture("medievalbooksnl_posters.html"))

        self.assertEquals(result.title, 'Medieval Posters | medievalbooks')
        self.assertEquals(result.description,
                          'In our modern society there are words everywhere around us, all the time. They are not '
                          'only written in books – that fair and most devoted carrier of text – but also on walls, '
                          'where they appear in all shapes and sizes. Judging from surviving paintings, it appears '
                          'that in medieval times it was less common to have words…')
        self.assertEquals(result.og_title, 'Medieval Posters')
        self.assertEquals(result.og_description,
                          'In our modern society there are words everywhere around us, all the time. They are not '
                          'only written in books – that fair and most devoted carrier of text – but also on walls, '
                          'where they appear in a...')

        self.assertEquals(result.og_image,
                          'https://medievalbooks.files.wordpress.com/2015/09/ambroggio_lorenzetti_detail.jpg?w=1200')
        self.assertEquals(result.og_image_width, 1200)
        self.assertEquals(result.og_image_height, 700)

        self.assertEquals(result.thumbnail_url,
                          'https://medievalbooks.files.wordpress.com/2015/09/ambroggio_lorenzetti_detail.jpg?w=1200')
        self.assertEquals(result.thumbnail_width, 1200)
        self.assertEquals(result.thumbnail_height, 700)
