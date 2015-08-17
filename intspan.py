
import sys
import copy
from itertools import groupby, count, chain
import re

__all__ = 'intspan spanlist intspanlist TheRest'.split()

_PY3 = sys.version_info[0] > 2
if _PY3:
    basestring = str


# Define regular expressions for spans and spans that may contain
# star (TheRest) markers
SPANRE = re.compile(r'^\s*(?P<start>-?\d+)\s*(-\s*(?P<stop>-?\d+))?\s*$')
SPANRESTAR = re.compile(
    r'^\s*((?P<star>\*)|(?P<start>-?\d+)\s*(-\s*(?P<stop>-?\d+))?)\s*$')


class ParseError(ValueError):
    pass


class Rester(object):

    """
    Singleton to represent "the rest of the values."
    """

    def __repr__(self):
        return 'TheRest'

    def __str__(self):
        return '*'


TheRest = Rester()


def _parse_range(datum):

    """
    Parser for intspan and intspan list.
    """

    def parse_chunk(chunk):
        """
        Parse each comma-separated chunk. Hyphens (-) can indicate ranges,
        or negative numbers. Returns a list of specified values. NB Designed
        to parse correct input correctly. Results of incorrect input are
        undefined.
        """
        m = SPANRESTAR.search(chunk)
        if m:
            if m.group('star'):
                return [TheRest]
            start = int(m.group('start'))
            if not m.group('stop'):
                return [start]
            stop = int(m.group('stop'))
            return list(range(start, stop + 1))
        else:
            raise ParseError("Can't parse chunk '{0}'".format(chunk))

    if isinstance(datum, basestring):
        result = []
        for part in datum.split(','):
            chunk = part.strip()
            if chunk:
                result.extend(parse_chunk(chunk))
        return result
    else:
        return datum if hasattr(datum, '__iter__') else [datum]


def spanlist(spec=None, chunkre=SPANRESTAR):
    """
    Given a string specification like the ones given to ``intspan``,
    return a list of the included items, in the same item given. Thus,
    ``spanlist("3,1-4")`` yields ``[3, 1, 2, 4]``. Experimental partial
    implementation of ability to have ordered intspans.
    """
    if spec is None or (isinstance(spec, basestring) and spec.strip() == ''):
        return []
    rawitems = _parse_range(spec)
    seen = set()
    items = []
    for i in rawitems:
        if i in seen:
            continue
        items.append(i)
        seen.add(i)
    return items


def _as_range(iterable):
    """
    Return a tuple representing the bounds of the range.
    """
    l = list(iterable)
    return (l[0], l[-1])


def _as_range_str(iterable):
    """
    Return a string representing the range as a string span.
    """
    l = list(iterable)
    if len(l) > 1:
        return '{0}-{1}'.format(l[0], l[-1])
    else:
        return '{0}'.format(l[0])


def _noRestDiff(a, b):
    """
    Special difference that, in case difference cannot be computed
    because of ``TypeError`` (indicating that a ``Rester`` object)
    has been found), returns a difference indicating the spanned items
    / group has ended.
    """
    try:
        return a - b
    except TypeError:
        return 2  # anything more than 1 signals "the next thing is in
                  # another span, not this current one"


class intspan(set):

    """
    The reason for the season.
    """

    def __init__(self, initial=None):
        super(intspan, self).__init__()
        if initial:
            self.update(initial)

    def copy(self):
        return copy.copy(self)

    def update(self, items):
        super(intspan, self).update(_parse_range(items))
        return self

    def intersection_update(self, items):
        super(intspan, self).intersection_update(_parse_range(items))
        return self

    def difference_update(self, items):
        super(intspan, self).difference_update(_parse_range(items))
        return self

    def symmetric_difference_update(self, items):
        super(intspan, self).symmetric_difference_update(
            _parse_range(items))
        return self

    def discard(self, items):
        for item in _parse_range(items):
            super(intspan, self).discard(item)

    def remove(self, items):
        for item in _parse_range(items):
            super(intspan, self).remove(item)

    def add(self, items):
        for item in _parse_range(items):
            super(intspan, self).add(item)

    def issubset(self, items):
        return super(intspan, self).issubset(_parse_range(items))

    def issuperset(self, items):
        return super(intspan, self).issuperset(_parse_range(items))

    def union(self, items):
        return intspan(super(intspan, self).union(_parse_range(items)))

    def intersection(self, items):
        return intspan(super(intspan, self).intersection(_parse_range(items)))

    def difference(self, items):
        return intspan(super(intspan, self).difference(_parse_range(items)))

    def symmetric_difference(self, items):
        return intspan(super(intspan, self).symmetric_difference(_parse_range(items)))

    __le__   = issubset
    __ge__   = issuperset
    __or__   = union
    __and__  = intersection
    __sub__  = difference
    __xor__  = symmetric_difference
    __ior__  = update
    __iand__ = intersection_update
    __isub__ = difference_update
    __ixor__ = symmetric_difference_update

    def __eq__(self, items):
        return super(intspan, self).__eq__(_parse_range(items))

    def __lt__(self, items):
        return super(intspan, self).__lt__(_parse_range(items))

    def __gt__(self, items):
        return super(intspan, self).__gt__(_parse_range(items))

    def __iter__(self):
        """
        Iterate in ascending order.
        """
        return iter(sorted(super(intspan, self).__iter__()))

    def pop(self):
        if self:
            min_item = min(self)
            self.discard(min_item)
            return min_item
        else:
            raise KeyError('pop from an empty set')

        # This method added only for PyPy, which otherwise would get the wrong
        # answer (unordered).

    def complement(self, low=None, high=None):
        """
        Return the complement of the given intspan--that is, all of the
        'missing' elements between its minimum and missing values.
        Optionally allows the universe set to be manually specified.
        """
        cls = self.__class__
        if not self:
            raise ValueError('cannot represent infinite set')
        low = low if low is not None else min(self)
        high = high if high is not None else max(self)
        universe = cls.from_range(low, high)
        return universe - self

    @classmethod
    def from_range(cls, low, high):
        """
        Construct an intspan from the low value to the high value,
        inclusive. I.e., closed range, not the more typical Python
        half-open range.
        """
        return cls(range(low, high + 1))

    @classmethod
    def from_ranges(cls, ranges):
        """
        Construct an intspan from a sequence of (low, high) value
        sequences (lists or tuples, say). Note that these values are
        inclusive, closed ranges, not the more typical Python
        half-open ranges.
        """
        return cls(chain(*(range(r[0], r[1] + 1) for r in ranges)))

    def __repr__(self):
        """
        Return the representation.
        """
        clsname = self.__class__.__name__
        return '{0}({1!r})'.format(clsname, self.__str__())

    def __str__(self):
        """
        Return the stringification.
        """
        items = sorted(self)
        gk = lambda n, c=count(): n - next(c)
        return ','.join(_as_range_str(g) for _, g in groupby(items, key=gk))

    def ranges(self):
        """
        Return a list of the set's contiguous (inclusive) ranges.
        """
        items = sorted(self)
        gk = lambda n, c=count(): n - next(c)
        return [_as_range(g) for _, g in groupby(items, key=gk)]

    # see Jeff Mercado's answer to http://codereview.stackexchange.com/questions/5196/grouping-consecutive-numbers-into-ranges-in-python-3-2
    # see also: http://stackoverflow.com/questions/2927213/python-finding-n-consecutive-numbers-in-a-list


# It might be interesting to have a metaclass factory that could create
# spansets of things other than integers. For example, enumerateds defined
# by giving a universe of possible options. Or characters. The Ranger
# package seems to do some of this http://pythonhosted.org/ranger/


class intspanlist(list):

    """
    An ordered version of ``intspan``. Is to ``list`` what ``intspan``
    is to ``set``, except that it is somewhat set-like, in that items
    are not intended to be repeated. Works fine as an immutable
    data structure. Still some issues if one mutates an instance. Not
    terrible problems, but the set-like nature where there is only
    one entry for each included integer may be broken.
    """

    def __init__(self, initial=None, universe=None):
        super(intspanlist, self).__init__()
        if initial:
            self.extend(initial)
        if universe is not None:
            try:
                restIndex = self.index(TheRest)
                remaining = sorted(intspan(universe) - set(self))
                self[restIndex + 1:restIndex + 1] = remaining  # splice
                self.pop(restIndex)
            except ValueError:
                pass

    def therest_update(self, universe, inplace=True):
        """
        If the receiving ``intspanlist`` contains a ``TheRest`` marker,
        replace it with the contents of the universe. Generally done
        *in situ*, but if value of ``inplace`` kwarg false, returns
        an edited copy.
        """
        toedit = self if inplace else self.copy()
        try:
            restIndex = toedit.index(TheRest)
            remaining = sorted(intspan(universe) - set(toedit))
            toedit[restIndex + 1:restIndex + 1] = remaining  # splice
            toedit.pop(restIndex)
        except ValueError:
            pass
        return toedit

    def copy(self):
        return copy.copy(self)

    def append(self, item):
        self.extend(spanlist(item))

    def extend(self, items):
        seen = set(self)
        for newitem in spanlist(items):
            if newitem in seen:
                continue
            super(intspanlist, self).append(newitem)

    def __eq__(self, items):
        return super(intspanlist, self).__eq__(spanlist(items))

    def __lt__(self, items):
        return super(intspanlist, self).__lt__(spanlist(items))

    def __gt__(self, items):
        return super(intspanlist, self).__gt__(spanlist(items))

    def complement(self, low=None, high=None):
        """
        Return the complement of the given intspanlist--that is, all of the
        'missing' elements between its minimum and missing values.
        Optionally allows the universe set to be manually specified.
        """
        cls = self.__class__
        if not self:
            raise ValueError('cannot represent infinite set')
        low = low if low is not None else min(self)
        high = high if high is not None else max(self)
        universe = cls.from_range(low, high)
        result = []
        contained = set(self)
        for x in universe:
            if x not in contained:
                result.append(x)
        return cls(result)

    @classmethod
    def from_range(cls, low, high):
        """
        Construct an intspan from the low value to the high value,
        inclusive. I.e., closed range, not the more typical Python
        half-open range.
        """
        return cls(range(low, high + 1))

    @classmethod
    def from_ranges(cls, ranges):
        """
        Construct an intspan from a sequence of (low, high) value
        sequences (lists or tuples, say). Note that these values are
        inclusive, closed ranges, not the more typical Python
        half-open ranges.
        """
        return cls(chain(*(range(r[0], r[1] + 1) for r in ranges)))

    def __repr__(self):
        """
        Return the representation.
        """
        clsname = self.__class__.__name__
        return '{0}({1!r})'.format(clsname, self.__str__())

    def __str__(self):
        """
        Return the stringification.
        """
        gk = lambda n, c=count(): _noRestDiff(n, next(c))
        return ','.join(_as_range_str(g) for _, g in groupby(self, key=gk))

    def ranges(self):
        """
        Return a list of the set's contiguous (inclusive) ranges.
        """
        gk = lambda n, c=count(): _noRestDiff(n, next(c))
        return [_as_range(g) for _, g in groupby(self, key=gk)]
