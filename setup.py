#!/usr/bin/env python

from setuptools import setup

required = [
    'astropy',
    'chimenea',  # use requirements.txt first.
    'click',
    'colorlog',
    'drive-ami',
    'drive-casa',
    'simplejson',
]

setup(
    name="amisurvey",
    version="0.5.0",
    packages=['amisurvey'],
    scripts=[
        'bin/amisurvey_makelist.py',
        'bin/amisurvey_reduce.py',
    ],
    description="An end-to-end calibration and imaging pipeline for "
                "data from the AMI-LA radio observatory.",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/amisurvey",
    install_requires=required,

)
