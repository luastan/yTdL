#!/usr/bin/python3
from setuptools import setup, find_packages

setup(name='ytdl',
      version='0.1',
      description='Download videos as mp3 from youtubeinmp3',
      url='http://github.com/luastan/',
      scripts=['ytdl'],
      packages=find_packages(),
      zip_safe=False)
