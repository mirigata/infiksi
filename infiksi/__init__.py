import bs4
import requests
import requests.exceptions


class InfiksiError(Exception):
    pass


class UnreachableError(InfiksiError):
    pass


class TemporaryError(InfiksiError):
    pass


class OEmbedResponse(object):
    def __init__(self, title=None, description=None, canonical_url=None, author_name=None,
                 og_title=None, og_description=None, og_image=None, og_image_width=None, og_image_height=None,
                 thumbnail_url=None, thumbnail_width=None, thumbnail_height=None,
                 ):
        self.canonical_url = canonical_url
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


def retrieve_html(url, timeout=1000):
    try:
        result = requests.get(url, timeout=(1.0 / timeout))
    except requests.exceptions.ConnectionError:
        raise UnreachableError("Could not reach {}".format(url))
    except requests.exceptions.TooManyRedirects:
        raise UnreachableError("Too many redirects while attempting to resolve {}".format(url))
    except requests.exceptions.RequestException:
        raise UnreachableError("Unknown error while trying to download {}".format(url))

    if result.status_code // 100 == 4:  # 4xx
        raise UnreachableError("Could not find page {}, got status code {}".format(url, result.status_code))

    if result.status_code // 100 == 5:  # 5xx
        raise TemporaryError("Could not find page {}, got status code {}".format(url, result.status_code))

    return result.text, result.url


def get_metadata(url, timeout=1000):
    html, effective_url = retrieve_html(url, timeout)
    return parse_contents(html, effective_url)


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


def parse_contents(html, effective_url=None):
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

        canonical_url=effective_url,

        og_title=og_title,
        og_description=og_description,

        og_image=og_image,
        og_image_width=og_image_width,
        og_image_height=og_image_height,
    )
