#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='video-motion',
    version='0.1',
    description='capture video on motion',
    author='Chris Lee',
    author_email='sihrc.c.lee@gmail.com',
    packages=find_packages(),
    install_requires=open(
        os.path.join(
            os.path.dirname(__file__),
            "requirements.txt"
        ),
        'r'
    ).readlines()
)
