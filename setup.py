#!/usr/bin/env python3

from setuptools import setup, find_packages


with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='navernewscrawler',
    version='0.0.3',
    description='Tool for crawling news on Naver',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ehsong/navernewscrawler',
    author=['Eunhou Esther Song'],
    author_email='eunhou.song@gmail.com',
    license='MIT',
    packages=find_packages(exclude=["build.*", "tests", "tests.*"]),
    install_requires=required,
    entry_points={
        "console_scripts": [
            "navernewscrawler = navernewscrawler.main:main"
        ]
    })
