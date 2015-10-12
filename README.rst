infiksi - Extracting metadata from websites
===========================================

A small library for extracting metadata from websites. A simple example:

::

    >>> from infiksi import get_metadata
    >>> response = get_metadata('http://www.wikipedia.org')
    >>> response.title
    'Wikipedia'

You can also use the ``server`` module to run this as a web service:

::

    $ python -m infiksi.server
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat

You can now request website metadata using ``curl``:

::

    $ curl http://localhost:5000/?q=https://www.wikipedia.org/
    {
      "author_name": null,
      "canonical_url": "https://www.wikipedia.org/",
      "description": null,
      "og_description": null,
      "og_image": null,
      "og_image_height": null,
      "og_image_width": null,
      "og_title": null,
      "thumbnail_height": null,
      "thumbnail_url": null,
      "thumbnail_width": null,
      "title": "Wikipedia",
      "type": "article",
      "version": "1.0"
    }
