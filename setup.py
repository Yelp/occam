# -*- coding: utf-8 -*-
from setuptools import setup

from occam.version import VERSION

setup(
    name="occam",
    version=VERSION,
    author="Fred Hatfull",
    author_email="fred.hatfull@gmail.com",
    description=("A simple Python library for interacting with Razor"),
    license="MIT",
    keywords="razor razor-server imaging library",
    url="https://github.com/fhats/occam",
    packages=['occam', 'tests'],
    long_description="A frontend to the Razor automated imager tool. See https://github.com/fhats/occam for more information.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Installation/Setup",
    ],
    install_requires=[
        "celery[redis] == 3.1.9",
        "python-dateutil == 2.2",
        "Flask == 0.10.0",
        "requests == 2.2.0",
        "py_razor_client == 0.1.2",
        "pyyaml == 3.10",
    ],
    tests_require=[
        "coverage == 3.7.1",
        "mock == 1.0.1",
        "testify == 0.5.2"
    ]
)
