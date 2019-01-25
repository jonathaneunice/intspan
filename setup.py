#!/usr/bin/env python

from setuptools import setup
from codecs import open


def lines(text):
    """
    Returns each non-blank line in text enclosed in a list.
    See http://pypi.python.org/pypi/textdata for more sophisticated version.
    """
    return [l.strip() for l in text.strip().splitlines() if l.strip()]


setup(
    name='intspan',
    version='1.5.15',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description="Sets of integers like 1,3-7,33",
    long_description=open('README.rst', encoding='utf-8').read(),
    url='https://bitbucket.org/jeunice/intspan',
    license='Apache License 2.0',
    packages=['intspan'],
    setup_requires=[],
    install_requires=[],
    tests_require=['tox', 'pytest', 'pytest-cov'],
    test_suite="test",
    zip_safe=False,
    keywords='integer set span range intspan intrange intspanlist',
    classifiers=lines("""
        Development Status :: 5 - Production/Stable
        Operating System :: OS Independent
        License :: OSI Approved :: Apache Software License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: 3.7
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Software Development :: Libraries :: Python Modules
    """)
)
