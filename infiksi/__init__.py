import bs4
import requests
import requests.exceptions

class UnreachableError(Exception):
    pass


class OEmbedResponse(object):
    def __init__(self, title=None, description=None, author_name=None,
                 og_title=None, og_description=None, og_image=None, og_image_width=None, og_image_height=None,
                 thumbnail_url=None, thumbnail_width=None, thumbnail_height=None,
                 ):
        self.og_image_height = og_image_height
        self.og_image_width = og_image_width
        self.og_image = og_image
        self.thumbnail_height = thumbnail_height
        self.thumbnail_width = thumbnail_width
        self.thumbnail_url = thumbnail_url
        self.author_name = author_name
        self.description = description
        self.og_title = og_title
        self.og_description = og_description
        self.title = title
        self.version = '1.0'
        self.type = 'article'

        if og_image and not thumbnail_url:
            self.thumbnail_url = og_image

            if og_image_width and not thumbnail_width:
                self.thumbnail_width = og_image_width
            if og_image_height and not thumbnail_height:
                self.thumbnail_height = og_image_height


def retrieve_html(url):
    try:
        result = requests.get(url)
    except requests.exceptions.ConnectTimeout:
        raise UnreachableError("Could not reach {}".format(url))

    return result.text


def get_metadata(url):
    html = retrieve_html(url)
    return parse_contents(html)


def _get_meta_contents_by_name(soup, name):
    meta_tags = soup.select("meta[name={}]".format(name))
    if not meta_tags:
        return None

    return meta_tags[0].attrs['content']


def _get_meta_contents_by_property(soup, prop):
    meta_tags = soup.select("meta[property={}]".format(prop))
    if not meta_tags:
        return None

    return meta_tags[0].attrs['content']


def parse_contents(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    title = soup.title.text if soup.title else None
    description = _get_meta_contents_by_name(soup, "description")
    author = _get_meta_contents_by_name(soup, "author")

    og_title = _get_meta_contents_by_property(soup, "og:title")
    og_description = _get_meta_contents_by_property(soup, "og:description")
    og_image = _get_meta_contents_by_property(soup, "og:image")
    og_image_width = _get_meta_contents_by_property(soup, "og:image:width")
    if og_image_width:
        og_image_width = int(og_image_width)
    og_image_height = _get_meta_contents_by_property(soup, "og:image:height")
    if og_image_height:
        og_image_height = int(og_image_height)

    return OEmbedResponse(
        title=title,
        description=description,
        author_name=author,

        og_title=og_title,
        og_description=og_description,

        og_image=og_image,
        og_image_width=og_image_width,
        og_image_height=og_image_height,
    )


