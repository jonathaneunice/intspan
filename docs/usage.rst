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

The ``universe`` method returns the covering set or "implied universe" of
an ``intspan``::

    >> intspan('1,3,5,7').universe()
    intspan('1-7')

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
