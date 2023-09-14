import codecs
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Yandex Alice Dialogs Utility'

setup(
    name="yadu",
    version=VERSION,
    author="NikshetSteh",
    author_email="<stehnikshet@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=["aiohttp", "aiohttp-wsgi"],
    keywords=["python", "alice", "bot", "yandex", "api"]
)
