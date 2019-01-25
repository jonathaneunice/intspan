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
could loop over that object in the desired order.(See below for a different
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
``intspanlist`` is a thinner shim over ``list``. It works well as an
immutable type, but modifications such as ``pop``, ``insert``, and slicing
are more problematic. ``append`` and ``extend`` work to maintain a
"set-ish," no-repeats nature--by discarding any additions that are already
in the container. Whatever was seen first is considered to be in its "right"
position. ``insert`` and other ``list`` update methods, however, provide no
such promises.

Indeed, it's not entirely clear what update behavior *should
be*, given the use case. If a duplicate is appended or inserted somewhere,
should an exception be raised? Should the code silently refuse to add items
already seen? Or something else? Maybe even duplicates should be allowed?
Silent denial is the current default, which is compatible with set behavior
and ``intspan``; whether that's the "right" or best choice for a fully ordered
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

If the universe is not given immediately, you may later update the
``intspanlist`` with it::

    >>> i = intspanlist('1-4,*,8')
    >>> i.therest_update('1-9')
    intspanlist('1-7,9,8')

If you don't wish to modify the original list (leaving its abstract
marker in place), a copy may be created by setting the ``inplace=False``
kwarg.

The abstract "and the rest" markers are intended to make ``intspanlist``
more convenient for specifying complex partial orderings.
