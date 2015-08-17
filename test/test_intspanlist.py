
import pytest
from intspan import *
from intspan import ParseError, TheRest


def test_TheRest_strings():
    assert str(TheRest) == '*'
    assert repr(TheRest) == 'TheRest'


def test_basic():
    s = intspanlist()
    tests = ['', '1', '1-2', '1-3,9-10', '1-3,14,29,92-97']
    for t in tests:
        s = intspanlist(t)
        assert str(s) == t


def test_lopsided_constructor():
    s = intspanlist('', '4-7')
    ss = intspanlist('*', '4-7')
    assert len(s) == 0
    assert len(ss) == 4


def test_parse_error():
    with pytest.raises(ParseError):
        s = intspanlist('7*99')
    with pytest.raises(ParseError):
        s = intspanlist('1-4,5-')


def test_negatives():
    assert list(intspanlist('-2')) == [-2]
    assert list(intspanlist('-2-1')) == [-2, -1, 0, 1]
    assert list(intspanlist('-2--1')) == [-2, -1]


def test_contains():
    s = intspanlist()
    assert 1 not in s
    assert 100 not in s
    assert 0 not in s

    t = intspanlist('1,10')
    assert 1 in t
    assert 10 in t
    assert 0 not in t
    assert 2 not in t


def test_equals():
    s = intspanlist('1,3,5,7,9')
    assert s == [1, 3, 5, 7, 9]


def test_lt_and_gt():
    s = intspanlist('1,2')
    t = intspanlist('1,2,4')
    u = intspanlist('4,5')
    assert s < t < u
    assert u > t > s
    assert u > s
    assert u > t
    assert s < t
    assert s < u
    assert t < u
    assert t > s


def test_copy():
    t = intspanlist('1,10,1-10')
    tt = t.copy()
    assert type(tt) == type(t)
    assert t == tt
    assert t is not tt


def test_len():
    s = intspanlist('1,2,3,5,8,13,21')
    assert len(s) == 7
    s.pop()
    assert len(s) == 6
    assert len(intspanlist()) == 0
    assert len(intspanlist('')) == 0
    assert len(intspanlist(1)) == 1
    assert len(intspanlist('1')) == 1
    assert len(intspanlist([1, 4])) == 2
    assert len(intspanlist('1,4')) == 2


def test_pop():
    s = intspanlist('100-110')
    assert s.pop(0) == 100
    assert s.pop(0) == 101
    assert s.pop(0) == 102
    assert s.pop(0) == 103
    assert s.pop(0) == 104
    assert s.pop(0) == 105
    assert s == intspanlist('106-110')

    s = intspanlist('1-2')
    assert s.pop(0) == 1
    assert s.pop(0) == 2
    with pytest.raises(IndexError):
        s.pop()


def test_append():
    s = intspanlist('100-110')
    assert len(s) == 11
    s.append(111)
    assert len(s) == 12
    assert s == intspanlist('100-111')

    # deviant add of already existing element
    s.append(111)
    assert len(s) == 12
    assert s == intspanlist('100-111')


def test_extend():
    s = intspanlist('100-110')
    assert len(s) == 11
    s.extend([111, 112])
    assert len(s) == 13
    assert s == intspanlist('100-112')

    # deviant add of already existing element
    s.extend([101, 112])
    assert len(s) == 13
    assert s == intspanlist('100-112')


def test_ranges_basic():
    assert intspanlist().ranges() == []
    assert intspanlist('2').ranges() == [(2, 2)]
    assert intspanlist('1-3').ranges() == [(1, 3)]
    assert intspanlist('1-3,5-6').ranges() == [(1, 3), (5, 6)]


def test_from_range():
    assert intspanlist.from_range(1, 3) == intspanlist('1-3')
    assert intspanlist.from_range(2, 44) == intspanlist('2-44')


def test_from_ranges():
    assert intspanlist.from_ranges([(1, 3), (5, 6)]) == intspanlist('1-3,5-6')
    assert intspanlist.from_ranges([(1, 3)]) == intspanlist('1-3')
    assert intspanlist.from_ranges([(4, 9), (1, 3)]) == intspanlist('4-9, 1-3')
    assert intspanlist.from_ranges([(2, 2)]) == intspanlist('2')
    assert intspanlist.from_ranges([]) == intspanlist()


def test_complement():
    s = intspanlist('1,3,5-9')
    assert s.complement() == intspanlist('2,4')
    assert s.complement(high=10) == intspanlist('2,4,10')
    assert s.complement(high=14) == intspanlist('2,4,10-14')
    assert s.complement(low=0) == intspanlist('0,2,4')
    assert s.complement(low=0, high=14) == intspanlist('0,2,4,10-14')

    # different order than intspan tested
    s = intspanlist('3,5-9,1,11')
    assert s.complement() == intspanlist('2,4,10')
    assert s.complement(high=12) == intspanlist('2,4,10,12')
    assert s.complement(high=14) == intspanlist('2,4,10,12-14')
    assert s.complement(low=0) == intspanlist('0,2,4,10')
    assert s.complement(low=0, high=14) == intspanlist('0,2,4,10,12-14')

    assert s.complement(-2, 5) == intspanlist('-2,-1,0,2,4')

    items = intspanlist('1-3,5,7-9,10,21-24')
    assert items.complement() == intspanlist('4,6,11-20')
    assert items.complement(high=30) == intspanlist('4,6,11-20,25-30')

    with pytest.raises(ValueError):
        intspanlist().complement()
        # cannot get the complement of an empty set


def test_repr_and_str():
    s = intspanlist('10-20,50-55')
    s.append(9)
    assert str(s) == intspanlist('10-20,50-55,9')
    s = intspanlist(s[3:])
    assert str(s) == '13-20,50-55,9'
    assert repr(s) == "intspanlist('" + str(s) + "')"


def test_spanlist():
    assert spanlist() == []
    assert spanlist(1) == [1]
    assert spanlist([33, 1, 3, 4]) == [33, 1, 3, 4]
    assert spanlist([33, 1, 3, 33, 4]) == [33, 1, 3, 4]
    assert spanlist('') == []
    assert spanlist('1') == [1]
    assert spanlist('33,1,3,4') == [33, 1, 3, 4]
    assert spanlist('33,1,3,33,4') == [33, 1, 3, 4]
    assert spanlist('4,1-5') == [4, 1, 2, 3, 5]
    assert spanlist('4,1-5,5') == [4, 1, 2, 3, 5]
    assert spanlist('4,1-5,5,5,1') == [4, 1, 2, 3, 5]


def test_spanlist_rest():

    assert spanlist('*') == [TheRest]
    assert spanlist('1,*') == [1, TheRest]
    assert spanlist('*,1') == [TheRest, 1]
    assert spanlist('33,*,1,3,4') == [33, TheRest, 1, 3, 4]
    assert spanlist('33,1,3,33,4,*') == [33, 1, 3, 4, TheRest]
    assert spanlist('4,1-5,*') == [4, 1, 2, 3, 5, TheRest]
    assert spanlist('4,*,1-5') == [4, TheRest, 1, 2, 3, 5]
    assert spanlist('4,*,1-5,5,*') == [4, TheRest, 1, 2, 3, 5]


def test_constructor():
    assert intspanlist() == []
    assert intspanlist(1) == [1]
    assert intspanlist([33, 1, 3, 4]) == [33, 1, 3, 4]
    assert intspanlist([33, 1, 3, 33, 4]) == [33, 1, 3, 4]
    assert intspanlist('') == []
    assert intspanlist('1') == [1]
    assert intspanlist('33,1,3,4') == [33, 1, 3, 4]
    assert intspanlist('33,1,3,33,4') == [33, 1, 3, 4]
    assert intspanlist('4,1-5') == [4, 1, 2, 3, 5]
    assert intspanlist('4,1-5,5') == [4, 1, 2, 3, 5]
    assert intspanlist('4,1-5,5,5,1') == [4, 1, 2, 3, 5]


def test_repr():
    assert repr(intspanlist()) == "intspanlist('')"
    assert repr(intspanlist(1)) == "intspanlist('1')"
    assert repr(intspanlist([33, 1, 3, 4])) == "intspanlist('33,1,3-4')"
    assert repr(intspanlist([33, 1, 3, 33, 4])) == "intspanlist('33,1,3-4')"
    assert repr(intspanlist('')) == "intspanlist('')"
    assert repr(intspanlist('1')) == "intspanlist('1')"
    assert repr(intspanlist('33,1,3,4')) == "intspanlist('33,1,3-4')"
    assert repr(intspanlist('33,1,3,33,4')) == "intspanlist('33,1,3-4')"
    assert repr(intspanlist('4,1-5')) == "intspanlist('4,1-3,5')"
    assert repr(intspanlist('4,1-5,5')) == "intspanlist('4,1-3,5')"
    assert repr(intspanlist('4,1-5,5,5,1')) == "intspanlist('4,1-3,5')"


def test_repr_star():
    # first without resolving TheRest
    assert repr(intspanlist('*')) == "intspanlist('*')"
    assert repr(intspanlist('1,*')) == "intspanlist('1,*')"
    assert repr(intspanlist('*,1')) == "intspanlist('*,1')"
    assert repr(intspanlist('33,1,*,3,4')) == "intspanlist('33,1,*,3-4')"
    assert repr(intspanlist('33,1,3,*,33,*,4')) == "intspanlist('33,1,3,*,4')"


def test_repr_star_resolved():
    assert repr(intspanlist('*')) == "intspanlist('*')"
    assert repr(intspanlist('1,*')) == "intspanlist('1,*')"
    assert repr(intspanlist('*,1')) == "intspanlist('*,1')"
    assert repr(intspanlist('33,1,*,3,4')) == "intspanlist('33,1,*,3-4')"
    assert repr(intspanlist('33,1,3,*,33,*,4')) == "intspanlist('33,1,3,*,4')"


def test_ranges():
    assert intspanlist('').ranges() == []
    assert intspanlist('1-14').ranges() == [(1, 14)]
    assert intspanlist('9,4,1-3,5-8,10-14').ranges() == \
        [(9, 9), (4, 4), (1, 3), (5, 8), (10, 14)]


def test_ranges_star():
    assert intspanlist('*').ranges() == [(TheRest, TheRest)]
    assert intspanlist('1-14, *').ranges() == [(1, 14), (TheRest, TheRest)]
    assert intspanlist('*,1-14').ranges() == [(TheRest, TheRest), (1, 14)]
    assert intspanlist('9,4,1-3,*,5-8,10-14').ranges() == \
        [(9, 9), (4, 4), (1, 3), (TheRest, TheRest), (5, 8), (10, 14)]


def test_ranges_resolved():
    assert intspanlist('*', '1-4') == [1, 2, 3, 4]
    assert intspanlist('1-4,*', '1-8') == [1, 2, 3, 4, 5, 6, 7, 8]
    assert intspanlist('*,1-4', '1-8') == [5, 6, 7, 8, 1, 2, 3, 4]
    assert intspanlist('5,*,1-4', '1-8') == [5, 6, 7, 8, 1, 2, 3, 4]
    assert intspanlist('6,*,1-4', '1-8') == [6, 5, 7, 8, 1, 2, 3, 4]
    assert intspanlist('*,6,*,1-4', '1-8') == [5, 7, 8, 6, 1, 2, 3, 4]


def test_star_doc_examples():
    assert intspanlist('1-4,*,8', '1-9') == intspanlist('1-7,9,8') == \
        [1, 2, 3, 4, 5, 6, 7, 9, 8]

    assert repr(intspanlist('1-4,*,8')) == "intspanlist('1-4,*,8')"
    assert repr(intspanlist('1-4,*,8', '1-9')) == "intspanlist('1-7,9,8')"

    i = intspanlist('1-4,*,8')
    i.therest_update('1-9')
    assert repr(i) == "intspanlist('1-7,9,8')"


def test_therest_update():
    i = intspanlist('1-5,*')
    assert i == [1, 2, 3, 4, 5, TheRest]

    i2 = i.therest_update('1-7', inplace=False)
    assert i2 == [1, 2, 3, 4, 5, 6, 7]
    assert i2 is not i

    i.therest_update('1-7')
    assert i == [1, 2, 3, 4, 5, 6, 7]
    assert i == i2
    assert i is not i2

    j = intspanlist('1,*,5')
    assert j == [1, TheRest, 5]

    j2 = j.therest_update('1-5', inplace=False)
    assert j2 == [1, 2, 3, 4, 5]
    assert j2 is not j

    j.therest_update('1-5')
    assert j == [1, 2, 3, 4, 5]
    assert j is not j2


def test_therest_update_nostar():
    # if no star in the intspanlist, no update
    i = intspanlist('1-5')
    i2 = i.therest_update('1-7', inplace=False)
    assert i == [1, 2, 3, 4, 5]
    assert i2 == [1, 2, 3, 4, 5]
    assert i2 is not i
