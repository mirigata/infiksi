import bs4


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

    return dict(
        title=title,
        description=description,
        author=author,

        og_title=og_title,
        og_description=og_description,
    )
