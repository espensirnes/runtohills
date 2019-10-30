#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, Extension
# To use a consistent encoding
from codecs import open
from os import path
import numpy as np

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
	long_description = f.read()

setup(
    name='runtohills',
    version='1.0.1',

    description='GUI for running economic experiments',
    long_description=long_description,

    url='https://github.com/espensirnes/runtohills',
    author='Espen Sirnes',
    author_email='espen.sirnes@uit.no',

    license='GPL-3.0',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Researchers',
        'Topic :: Economic experiments',
        'License :: OSI Approved :: GPL-3.0 License',
        'Programming Language :: Python :: 3.7',
        ],


    keywords='Experiments, economics',
    packages=find_packages(),
    install_requires=['arcade'],
	python_requires='>=3.6',
	entry_points={
	    'console_scripts': [
	        'runtohills=runtohills:main',
	        ],
	    },	


)