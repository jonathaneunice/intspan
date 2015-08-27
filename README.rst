
| |travisci| |version| |downloads| |versions| |impls| |wheel| |coverage| |br-coverage|

.. |travisci| image:: https://api.travis-ci.org/jonathaneunice/intspan.svg
    :target: http://travis-ci.org/jonathaneunice/intspan

.. |version| image:: http://img.shields.io/pypi/v/intspan.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/intspan

.. |downloads| image:: http://img.shields.io/pypi/dm/intspan.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/intspan

.. |versions| image:: https://img.shields.io/pypi/pyversions/intspan.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/intspan

.. |impls| image:: https://img.shields.io/pypi/implementation/intspan.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/intspan

.. |wheel| image:: https://img.shields.io/pypi/wheel/intspan.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/intspan

.. |coverage| image:: https://img.shields.io/badge/test_coverage-100%25-6600CC.svg
    :alt: Test line coverage
    :target: https://pypi.python.org/pypi/intspan

.. |br-coverage| image:: https://img.shields.io/badge/branch_coverage-100%25-6600CC.svg
    :alt: Test branch coverage
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

There is also an ordered ``intspanlist`` type that helps specify the
ordering of a set of elements.

For this and more, see the full details on `Read the Docs
<http://intspan.readthedocs.org/en/latest/>`_.
