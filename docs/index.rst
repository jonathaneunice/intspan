intspan
=======

``intspan`` is a ``set`` subclass that conveniently represents sets of integers.
Sets can be created from and displayed as integer spans such as
``1-3,14,29,92-97`` rather than exhaustive member listings. Compare::

    intspan('1-3,14,29,92-97')
    [1, 2, 3, 14, 29, 92, 93, 94, 95, 96, 97]

Or worse, the unsorted, non-intuitive listings that crop up with Python's
native unordered sets, such as::

    set([96, 1, 2, 3, 97, 14, 93, 92, 29, 94, 95])

While they all indicate the same values, ``intspan`` output is much more compact
and comprehensible. It better divulges the contiguous nature of segments of the
collection, making it easier for humans to quickly determine the "shape" of the
data and ascertain "what's missing?"

When iterating, ``pop()``-ing an item, or converting to a list, ``intspan``
behaves as if it were an ordered--in fact, sorted--collection. A key
implication is that, regardless of the order in which items are added,
an ``intspan`` will always be rendered in the most compact, organized
form possible.

The main draw is having a convenient way to specify, manage, and see output in
terms of ranges--for example, rows to process in a spreadsheet. It can also help
you quickly identify or report which items were *not* successfully processed in
a large dataset.

.. toctree::
   :titlesonly:

   Usage <usage>
   intspanlist <intspanlist>
   Performance and Alternatives <issues>
   Notes <notes>
   API Reference <api>
   Installation <installation>
   CHANGES
