
| |travisci| |version| |downloads| |supported-versions| |supported-implementations| |wheel| |coverage|

.. |travisci| image:: https://api.travis-ci.org/jonathaneunice/intspan.svg
    :target: http://travis-ci.org/jonathaneunice/intspan

.. |version| image:: http://img.shields.io/pypi/v/intspan.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/intspan

.. |downloads| image:: http://img.shields.io/pypi/dm/intspan.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/intspan

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/intspan.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/intspan

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/intspan.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/intspan

.. |wheel| image:: https://img.shields.io/pypi/wheel/intspan.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/intspan

.. |coverage| image:: https://img.shields.io/badge/test_coverage-100%25-6600CC.svg
    :alt: Test line coverage
    :target: https://pypi.python.org/pypi/intspan


``intspan`` is a ``set`` subclass that conveniently stores sets of integers.
Sets can be created from and displayed as integer spans such as
``1-3,14,29,92-97`` rather than exhaustive member listings. Compare::

    intspan('1-3,14,29,92-97')
    [1, 2, 3, 14, 29, 92, 93, 94, 95, 96, 97]

While they indicate the same values, the ``intspan`` is more compact.
Even more important, it
better divulges the contiguous nature of parts of the collection. It
is easier for humans to quickly determine the "shape" of the collection
and ascertain "what's missing?"

When iterating, ``pop()``-ing an item, or converting to a list, ``intspan``
behaves as if it were an ordered--in fact, sorted--collection. A key
implication is that, regardless of the order in which items are added,
an ``intspan`` will always be rendered in the most compact, organized
form possible.

The main draw is having a convenient way to specify (possibly discontinuous)
ranges--for example, rows to process in a spreadsheet. It can also help you
quickly identify or report which items were *not* successfully processed in
a large dataset.

Usage
=====

::

    from intspan import intspan

    s = intspan('1-3,14,29,92-97')
    s.discard('2,13,92')
    print s
    print repr(s)
    print list(s)

yields::

    1,3,14,29,93-97
    intspan('1,3,14,29,93-97')
    [1, 3, 14, 29, 93, 94, 95, 96, 97]

While::

    >>> for n in intspan('1-3,5'):
    >>>     print n                 # Python 2
    1
    2
    3
    5

Most set operations such as intersection, union, and so on are available just
as they are in Python's ``set``. In addition, if you wish to extract the
contiguous ranges::

    >>> for r in intspan('1-3,5,7-9,10,21-22,23,24').ranges():
    >>>     print r                 # Python 2
    (1, 3)
    (5, 5)
    (7, 10)
    (21, 24)

Note that these endpoints represent
`closed intervals <http://en.wikipedia.org/wiki/Interval_(mathematics)>`_,
rather than the half-open intervals commonly used with Python's ``range()``.
If you combine ``intspan`` ranges with Python generators, you'll
have to increment the stop value by one yourself to create the suitable
"half-open interval."

There is a corresponding range-oriented constructor::

    >>> intspan.from_ranges([ (4,6), (10,12) ])
    intspan('4-6,10-12')

A convenience ``from_range`` method creates a contiguous
``intspan`` from a given low to a high value.::

    >>> intspan.from_range(8, 12)
    intspan('8-12')

To find the elements *not* included, you can use the ``complement`` method::

    >>> items = intspan('1-3,5,7-9,10,21-24')
    >>> items.complement()
    intspan('4,6,11-20')

The "missing" elements are computed as any integers between the
``intspan``'s minimum and maximum values that aren't included. If you'd like
to customize the intended ``low`` and ``high`` bounds, you can give those
explicitly.::

    >>> items.complement(high=30)
    intspan('4,6,11-20,25-30')

You can use the ``difference`` method or ``-`` operator
to find the complement with respect to an arbitrary set, rather than just
an expected contiguous range.

intspanlist
===========

As of version 1.2, a new function ``spanlist`` is provided. It
returns a list from the same kind of specification string ``intspan`` does,
but ordered as given rather than fully sorted. A corresponding
``intspanlist`` class subclasses ``list`` in
the same way that ``intspan`` subclasses ``set``. ::

    >>> intspanlist('4,1-5,5')  # note order preserved
    intspanlist('4,1-3,5')

    >>> list(intspanlist('4,1-5,5'))
    [4, 1, 2, 3, 5]

    >>> spanlist('4,1-5,5')
    [4, 1, 2, 3, 5]

So ``spanlist`` the function creates a ``list``, whereas ``intspanlist``
creates a similar object--but one that has a more sophisticated representation
and more specific update methods. Both of them have somewhat set-like behavior,
in that they seek to not have excess duplication of members.

The intended use for this strictly-ordered version of ``intspan`` is to
specify an ordering of elements. For example, a program might have 20 items,
1-20. If you wanted to process item 7, then item 3, then "all the rest,"
``intspanlist('7,3,1-20')`` would be a convenient way to specify this. You
could loop over that object in the desired order. (See below for a different
formulation, ``intspanlist('7,3,*')``, in which the ``*`` is a symbolic "all
the rest" marker, and the universe set can be specified either immediately
or later.)

Note that ``intspanlist`` objects do not necessarily display as they are
entered::

    >>> intspanlist('7,3,1-20')
    intspanlist('7,3,1-2,4-6,8-20')

This is an equivalent representation--though lower-level, more explicit, and
more verbose.

Many other ``list`` methods are available to ``intspanlist``, especially
including iteration. Note however that while ``intspan`` attempts to
faithfully implement the complete methods of a Python ``set`` ,
``intspanlist`` is a thiner shim over ``list``. It works well as an
immutable type, but modifications such as ``pop``, ``insert``, and slicing
are more problematic. ``append`` and ``extend`` work to maintain a
"set-ish," no-repeats nature--by discarding any additions that are already
in the container. Whatever was seen first is considered to be in its "right"
position. ``insert`` and other ``list`` update methods, however, provide no
such promises.

Indeed, it's not entirely clear what update behavior *should
be*, given the use case. If a duplicate is appended or inserted somewhere,
should an exception be raised? Should the code silent refuse to add items
already seen? Or something else? Maybe even duplicates should be allowed?
Silent denial is the current default, which is compatible with set behavior
and ``intspan``; whether that's the "right" choice for a fully ordered
variant is unclear. (If you have thoughts on this or relevant use cases to
discuss, open an issue on Bitbucket or ping the author.)

Symbolic Rest
-------------

As a final trick, ``intspanlist`` instances can contain a special value,
rendered as an asterisk (``*``), meaning "the rest of the list." Under
the covers, this is converted into the singleton object ``TheRest``.

    >>> intspanlist('1-4,*,8')
    intspanlist('1-4,*,8')

This symbolic "everything else" can be a convenience, but eventually it
must be "resolved."

``intspanlist`` objects may be created with an optional second parameter
which provides "the universe of all items" against which "the rest" may
be evaluated. For example::

    >>> intspanlist('1-4,*,8', '1-9')
    intspanlist('1-7,9,8')

Whatever items are "left over" from the universe set are included wherever
the asterisk appears. Like the rest of ``intspan`` and ``intspanlist``
constructors, duplicates are inherently removed.

If the universe is not given immeidately, you may later update the
``intspanlist`` with it::

    >>> i = intspanlist('1-4,*,8')
    >>> i.therest_update('1-9')
    intspanlist('1-7,9,8')

If you don't wish to modify the original list (leaving its abstract
marker in place), a copy may be created by setting the ``inplace=False``
kwarg.

The abstract "and the rest" markers are intended to make ``intspanlist``
more convenient for specifying complex partial orderings.

Performance and Alternatives
============================

The ``intspan`` module piggybacks Python's ``set`` and ``list`` types. So
it stores every integer individually. Unlike Perl's ``Set::IntSpan`` it is
not optimized for long contiguous runs. For sets of several hundred or even
many thousands of members, you will probably never notice the difference.

But if you're doing extensive processing of large sets (e.g.
with 100K, 1M, or more elements), or doing lots of set operations on them
(e.g. union, intersection), a data structure based on
lists of ranges, `run length encoding
<http://en.wikipedia.org/wiki/Run-length_encoding>`_, or `Judy arrays
<http://en.wikipedia.org/wiki/Judy_array>`_ might perform and scale
better. Horses for courses.

There are several modules you might want to consider as alternatives or
supplements. AFAIK, none of them provide the convenient integer span
specification that ``intspan`` does, but they have other virtues:

* `cowboy <http://pypi.python.org/pypi/cowboy>`_ provides
  generalized ranges and multi-ranges. Bonus points for the package
  tagline: "It works on ranges."

* `ranger <http://pypi.python.org/pypi/ranger>`_ is a generalized range and range set
  module. It supports open and closed ranges, and includes mapping objects that
  attach one or more objects to range sets.

* `rangeset <http://pypi.python.org/pypi/rangeset>`_ is a generalized range set
  module. It also supports infinite ranges.

* `judy <http://pypi.python.org/pypi/judy>`_ a Python wrapper around Judy arrays
  that are implemented in C. No docs or tests to speak of.

* `RoaringBitmap <https://pypi.python.org/pypi/roaringbitmap>`_, a
  hybrid array and bitmap structure designed for efficient compression
  and fast operations on sets of 32-bit integers.

Notes
=====

* See ``CHANGES.rst`` for a historical view of changes.

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


Installation
============

To install or upgrade to the latest version::

    pip install -U intspan

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade intspan

(You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide.)
