#!/usr/bin/env python

from setuptools import setup

required = ['simplejson',
            'colorlog',
            'drive-ami',
            'chimenea'
            ]

setup(
    name="amisurvey",
    version="0.3.4",
    packages=['amisurvey'],
    scripts=['bin/amisurvey_reduce.py'],
    description="An end-to-end calibration and imaging pipeline for "
                "data from the AMI-LA radio observatory.",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/amisurvey",
    install_requires=required,
)
