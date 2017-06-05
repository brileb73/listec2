#!/usr/bin/env python
"""
Setup script for installing using pip
"""
# pylint:disable=redefined-builtin
from codecs import open
from os import path
from setuptools import setup


def main():
    """
    Run setuptools.setup with README contents as long_description
    """
    base_dir = path.dirname(__file__)
    setup(
        name='listec2',
        version='0.1',
        description='AWS EC2 filter and display running instances',
        long_description=open(path.join(base_dir, 'README.rst'), encoding='utf-8').read(),
        author='Brian LeBlanc',
        author_email='brian.leblanc@bluespurs.com',
        license='Apache License 2.0',
        packages=['listec2'],
        install_requires=['boto3', 'six', 'tabulate'],
        entry_points={
            'console_scripts': [
                'listec2=listec2.main:main'
            ]
        }
    )


if __name__ == '__main__':
    main()
