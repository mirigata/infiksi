from codecs import open
from os import path

from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='infiksi',

    version='0.0.1',

    description='Extract metadata from web pages',
    long_description=long_description,

    url='https://github.com/mirigata/infiksi',

    author='Yigal Duppen',
    author_email='yigal@publysher.nl',

    license='AGPL',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='metadata',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=[
        'beautifulsoup4',
        'requests',
    ],

    extras_require = {
        'server': ['flask'],
    },

    test_suite="tests",
)
