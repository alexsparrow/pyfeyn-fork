#! /usr/bin/env python

"""PyFeyn: an easy-to-use Python library to help high-energy physicists draw Feynman diagrams."""

## Get setuptools
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

longdesc = """PyFeyn is a package which makes drawing Feynman diagrams simple and programmatic.
Feynman diagrams are important constructs in perturbative field theory, so being able to draw them
in a programmatic fashion is important if attempting to enumerate a large number of diagram
configurations is important. The output quality of PyFeyn diagrams (into PDF or EPS formats)
is very high, and special effects can be obtained by using constructs from PyX, which PyFeyn
is based around."""

## Setup definition
setup(name = 'pyfeyn',
      version = '0.3.0',
      packages = ['pyfeyn'],
      install_requires = ['pyx >= 0.9'],
      scripts = ['feynml-build'],
      author = 'Andy Buckley',
      author_email = 'andy@insectnation.org',
      url = 'http://projects.hepforge.org/pyfeyn/',
      description = 'An easy-to-use Python library to help physicists draw Feynman diagrams.',
      long_description = longdesc,
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
