from unittest import TestCase
import infiksi


class ContentExtractionTest(TestCase):

    def test_extract_empty_html(self):
        html = """
        <html></html>
        """
        result = infiksi.parse_contents(html)
        self.assertIsNotNone(result)

    def test_extract_from_title(self):
        html = """
        <html><head><title>My Beautiful Page</title></head></html>
        """

        result = infiksi.parse_contents(html)
        self.assertIsNotNone(result)
        self.assertEquals(result['title'], 'My Beautiful Page')

    def test_extract_from_livecodingtv(self):
        html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <title>Python: retrieving metadata from websites</title>
  <meta name="description" content=>
  <meta property="og:site_name" content="Livecoding.tv"/>
  <meta property="og:title" content="watch people code products live"/>
  <meta property="og:description" content="Python: retrieving metadata from websites"/>
  <meta property="og:image" content="/static/img/userdashboard-img.png?h=96c35f43"/>
  <meta property="og:url" content="/publysher/"/>
  <meta property="og:type" content="streaming platform"/>
</head><body>...</body></html>
        """

        result = infiksi.parse_contents(html)
        self.assertIsNotNone(result)

        self.assertEquals(result['title'], 'Python: retrieving metadata from websites')
        self.assertEquals(result['description'], None)
        self.assertEquals(result['og_title'], 'watch people code products live')
        self.assertEquals(result['og_description'], 'Python: retrieving metadata from websites')
