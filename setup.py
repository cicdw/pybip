#!/usr/bin/env python

from setuptools import setup


setup(name='pybip',
      version='0.0.1',
      description='Binary Integer Programming (BIP) experiments',
      url='https://github.com/moody-marlin/pybip.git',
      maintainer='Chris White',
      maintainer_email='white.cdw@gmail.com',
      packages=['pybip'],
      install_requires=list(open('requirements.txt').read().strip().split('\n')),
      zip_safe=False)
