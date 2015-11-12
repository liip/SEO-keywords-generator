#!/usr/bin/env python
from setuptools import find_packages

from setuptools import setup

setup(
    name='kwg',
    version='0.1',
    description='Keywords generator : based on patterns, generate a list of keyphrases for SEO tools such as AWR Cloud',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
        'click>=3.3',
    ],
    entry_points={
        'console_scripts': 'kwgen=keyword_generator.commands.base:cli'
    },
)

