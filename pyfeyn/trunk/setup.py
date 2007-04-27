#! /usr/bin/env python

## Get setuptools
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

## Setup definition
setup(name = 'pyfeyn',
      version = '0.3.0',
      packages = ['pyfeyn'],
      install_requires = 'pyx >= 0.9',
      author = 'Andy Buckley',
      author_email = 'andy@insectnation.org',
      url = 'http://projects.hepforge.org/pyfeyn/',
      description = 'An easy-to-use Python library to help high-energy physicists draw Feynman diagrams.',
      keywords = 'feynman hep physics particle diagram',
      license = 'GPL',
      classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Artistic Software',
                   'Topic :: Scientific/Engineering :: Physics']
      )
