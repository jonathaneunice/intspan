#! /usr/bin/env python
from setuptools import setup

def linelist(text):
    """
    Returns each non-blank line in text enclosed in a list.
    """
    return [ l.strip() for l in text.strip().splitlines() if l.strip() ]


setup(
    name='intspan',
    version='1.2.5',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description="Sets of integers like 1,3-7,33",
    long_description=open('README.rst').read(),
    url='https://bitbucket.org/jeunice/intspan',
    py_modules=['intspan'],
    install_requires=[],
    tests_require = ['tox', 'pytest', 'pytest-cov'],
    zip_safe = True,
    keywords='integer set span range intspan intrange intspanlist',
    classifiers=linelist("""
        Development Status :: 5 - Production/Stable
        Operating System :: OS Independent
        License :: OSI Approved :: BSD License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Software Development :: Libraries :: Python Modules
    """)
)
