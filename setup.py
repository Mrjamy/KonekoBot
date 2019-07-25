#!/usr/bin/env python3

# Builtins
from setuptools import setup

setup(
    name='KonekoBot',
    version='v1.1.0',
    packages=['src', 'src.cogs', 'src.utils', 'src.utils.user',
              'src.utils.random', 'src.utils.database',
              'src.utils.database.models', 'src.utils.database.repositories',
              'tests', 'tests.utils', 'tests.utils.games'],
    url='',
    license='MIT',
    author='Jamy',
    author_email='',
    description='A discord bot written in python'
)
