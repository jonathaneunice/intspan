Performance and Alternatives
============================

``intspan`` piggybacks Python's ``set`` type. ``inspanlist`` piggybacks
``list``. So it stores every integer individually. Unlike Perl's
``Set::IntSpan`` it is not optimized for long contiguous runs. For sets of
several hundred or even many thousands of members, you will probably never
notice the difference.

But if you're doing extensive processing of large sets (e.g.
with 100K, 1M, or more elements), or doing numeroius set operations on them
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
  tagline: "It works on ranges

* `spans <https://pypi.python.org/pypi/Spans>`_ provides several different
  kinds of ranges and then sets for those ranges. Includes nice ``datetime``
  based intervals similar to PostgreSQL time intervals, and ``float``
  ranges/sets. More ambitious and general than ``intspan``, but lacks truly
  convenient input or output methods akin to ``intspan``.

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
