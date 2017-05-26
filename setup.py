from os import path
from codecs import open
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = "defaultcontext",
    version = "1.0.0",
    author = "Bogdan Kulynych",
    author_email = "hello@bogdankulynych.me",
    description = "Util for creating tensorflow-like default context managers",
    license = "MIT",
    keywords = "utils",
    packages=find_packages(exclude=["tests"]),
    long_description=long_description,
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    test_require = ['pytest', 'tox']
)
