Notes
=====

* Though inspired by Perl's `Set::IntSpan <http://search.cpan.org/~swmcd/Set-IntSpan/IntSpan.pm>`_,
  that's where the similarity stops.
  ``intspan`` supports only finite sets, and it
  follows the methods and conventions of Python's ``set``.

* ``intspan`` methods and operations such as ``add()`` ``discard()``, and
  ``>=`` take integer span strings, lists, and sets as arguments, changing
  facilities that used to take only one item into ones that take multiples,
  including arguments that are technically string specifications rather than
  proper ``intspan`` objects.

* A version of ``intspanlist`` that does not discard duplicates is under
  consideration.

* String representation and ``ranges()`` method
  based on Jeff Mercado's concise answer to `this
  StackOverflow question <http://codereview.stackexchange.com/questions/5196/grouping-consecutive-numbers-into-ranges-in-python-3-2>`_.
  Thank you, Jeff!

* Automated multi-version testing managed with `pytest
  <http://pypi.python.org/pypi/pytest>`_, `pytest-cov
  <http://pypi.python.org/pypi/pytest-cov>`_,
  `coverage <https://pypi.python.org/pypi/coverage/4.0b1>`_
  and `tox
  <http://pypi.python.org/pypi/tox>`_. Continuous integration testing
  with `Travis-CI <https://travis-ci.org/jonathaneunice/intspan>`_.
  Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

  Successfully packaged for, and
  tested against, all late-model versions of Python: 2.6, 2.7, 3.2, 3.3,
  3.4, and 3.5 pre-release (3.5.0b3) as well as PyPy 2.6.0 (based on
  2.7.9) and PyPy3 2.4.0 (based on 3.2.5). Test line coverage 100%.

* The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
  `@jeunice on Twitter <http://twitter.com/jeunice>`_
  welcomes your comments and suggestions.

* If you find ``intspan`` useful, consider buying me a pint and a nice
  salty pretzel.

.. image:: https://img.shields.io/gratipay/jeunice.svg
    :target: https://www.gittip.com/jeunice/

