#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Inventory RESTful endpoints for vLab
"""
from setuptools import setup, find_packages


setup(name="vlab-inventory-api",
      author="Nicholas Willhite,",
      author_email='willnx84@gmail.com',
      version='2019.06.18',
      packages=find_packages(),
      include_package_data=True,
      package_files={'vlab_inventory_api' : ['app.ini']},
      description="An API for dealing with virtual inventory",
      install_requires=['flask', 'pyjwt', 'uwsgi', 'vlab-api-common', 'ujson',
                        'cryptography', 'vlab-inf-common', 'celery']
      )
