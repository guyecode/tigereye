#!/usr/bin/env python
# coding: utf8
import os
from setuptools import setup

requirements = open(
    os.path.join(os.path.dirname(__file__),
                 'requirements.txt')).readlines()

setup(
    name='tigereye',
    version='0.1',
    description=u'虚拟接入商',
    packages=['tigereye'],
    install_requires=requirements,
)
