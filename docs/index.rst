intspan
=======

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

.. toctree::
   :titlesonly:

   Usage <usage>
   intspanlist <intspanlist>
   Performance and Alternatives <issues>
   Notes <notes>
   API Reference <api>
   Installation <installation>
   CHANGES
