#! /usr/bin/env python

from setuptools import setup

setup(name = 'pyfeyn',
      version = '0.2.0b1',
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
