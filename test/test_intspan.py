
import pytest
from intspan import *
from intspan import ParseError


def test_basic():
    s = intspan()
    tests = ['', '1', '1-2', '1-3,9-10', '1-3,14,29,92-97']
    for t in tests:
        s = intspan(t)
        assert str(s) == t


def test_alt_contstructors():
    assert intspan(range(100)) == intspan('0-99')
    assert intspan([1,3,5]) == intspan('1,3,5')
    assert intspan([5,3,1]) == intspan('1,3,5')
    assert intspan(intspan('1,3,5')) == intspan('1,3,5')


def test_parse_error():
    with pytest.raises(ParseError):
        s = intspan('7*99')
    with pytest.raises(ParseError):
        s = intspan('1-4,5-')


def test_spaces():
    assert list(intspan('  ')) == []
    assert list(intspan('     1')) == [1]
    assert list(intspan('1, 4,  4 , 9')) == [1, 4, 9]
    assert list(intspan('1, 4, 4 , 9')) == [1, 4, 9]
    assert list(intspan('1, 4, 4 , 9')) == [1, 4, 9]
    assert list(intspan('   1, \n4,\n 4 , 9')) == [1, 4, 9]


def test_negatives():
    assert list(intspan('-2')) == [-2]
    assert list(intspan('-2-1')) == [-2, -1, 0, 1]
    assert list(intspan('-2--1')) == [-2, -1]


def test_contains():
    s = intspan()
    assert 1 not in s
    assert 100 not in s
    assert 0 not in s

    t = intspan('1,10')
    assert 1 in t
    assert 10 in t
    assert 0 not in t
    assert 2 not in t


def test_equals():
    s = intspan('1,3,5,7,9')
    assert s == set([1, 3, 5, 7, 9])


def test_strict_super_or_subset():
    s = intspan('1,3,5,7,9')
    t = intspan('1,3,5')
    u = intspan('0,1,3,5')
    assert s > t
    assert not s > u
    assert t < s
    assert t < u
    assert u > t
    assert not s < u
    assert not s > u


def test_isdisjoint():
    s = intspan('1,3,5,7,9')
    t = intspan('33-44')
    u = intspan('1,3,99,299')
    assert s.isdisjoint(t)
    assert not s.isdisjoint(u)
    assert t.isdisjoint(u)


def test_copy():
    t = intspan('1,10')
    tt = t.copy()
    assert type(tt) == type(t)
    assert t == tt
    assert t is not tt


def test_clear():
    s = intspan('1,2,3,5,8,13,21')
    s.clear()
    assert s == intspan()


def test_len():
    s = intspan('1,2,3,5,8,13,21')
    assert len(s) == 7
    s.pop()
    assert len(s) == 6
    s.clear()
    assert len(s) == 0


def test_merge():
    assert str(intspan('1-4,5')) == '1-5'


def test_out_of_order():
    assert str(intspan('1,0,99,4,7,9,98')) == '0-1,4,7,9,98-99'


def test_discard():
    s = intspan('1-3,14,29,92-97')
    s.discard('2,13,92')
    assert str(s) == '1,3,14,29,93-97'


def test_remove():
    s = intspan('1-3,14,29,92-97')
    s.remove('2,92')
    assert str(s) == '1,3,14,29,93-97'
    with pytest.raises(KeyError):
        s.remove(1000)


def test_add():
    s = intspan('1-2')
    s.add('3,29')
    assert str(s) == '1-3,29'
    s.add('92,97,96,95,94')
    assert str(s) == '1-3,29,92,94-97'
    s.add(93)
    assert str(s) == '1-3,29,92-97'
    s.add('14')
    assert str(s) == '1-3,14,29,92-97'


def test_iteration():
    s = intspan('92,97,96,95,0,94')
    assert [item for item in s] == [0, 92, 94, 95, 96, 97]
    assert list(s) == [0, 92, 94, 95, 96, 97]
    assert set(s) == set([0, 92, 94, 95, 96, 97])


def test_issubset():
    s = intspan('92,97,96,95,0,94')
    assert s.issubset('0-100')
    assert s.issubset(range(98))
    assert s.issubset(range(101))
    assert s.issubset('0, 92-100')
    assert s.issubset([0] + list(range(92, 101)))
    assert s.issubset(intspan('92,97,96,95,0,94'))
    assert s.issubset([0, 92, 94, 95, 96, 97])
    assert not s.issubset('0-10')
    assert not s.issubset(range(20))
    assert not s.issubset(range(95))


def test_issuperset():
    s = intspan('0-3,7')
    assert s.issuperset('0-2')
    assert s.issuperset([0, 1, 3])
    assert not s.issuperset(range(6))
    assert not s.issuperset('0-6')

    assert s >= intspan('0-2')
    assert s >= intspan([0, 1, 3])
    assert not s >= range(6)
    assert not s >= intspan('0-6')


def test_union():
    s = intspan('0-3,7')
    assert s.union('0-2') == s
    assert list(s.union('0-2')) == [0, 1, 2, 3, 7]
    assert list(s.union([99, 101])) == [0, 1, 2, 3, 7, 99, 101]
    assert s.union([99, 101]) == intspan('0-3,7,99,101')

    assert s | intspan('0-2') == s.union('0-2')
    assert s | [99, 101] == s.union('99,101')


def test_intersection():
    s = intspan('1-8')
    t = intspan('2-5')
    u = intspan('8,100')
    assert s.intersection(t) == intspan('2-5')
    assert t.intersection(u) == intspan()
    assert s.intersection(u) == intspan('8')

    assert s & t == s.intersection(t)
    assert t & u == t.intersection(u)
    assert s & u == s.intersection(u)


def test_difference():
    s = intspan('1-8')
    t = intspan('2-5')
    assert s.difference(t) == intspan('1,6-8')
    assert t.difference(s) == intspan()

    assert s - t == s.difference(t)
    assert t - s == t.difference(s)


def test_symmetric_difference():
    s = intspan('1-8')
    t = intspan('2-5')
    assert s.symmetric_difference(t) == intspan('1,6-8')
    assert t.symmetric_difference(s) == intspan('1,6-8')
    assert t.symmetric_difference(t) == intspan()

    assert s ^ t == s.symmetric_difference(t)
    assert t ^ s == t.symmetric_difference(s)
    assert t ^ t == t.symmetric_difference(t)


def test_augmented_assignments():
    s = intspan('50-60')
    s |= intspan('10-20')
    assert s == intspan('10-20,50-60')
    s &= intspan('0-55')
    assert s == intspan('10-20,50-55')
    s -= intspan('16-20')
    assert s == intspan('10-15,50-55')
    s ^= intspan('10,99')
    assert s == intspan('11-15,50-55,99')

    t = intspan('50-60')
    t.update('10-20')
    assert t == intspan('10-20,50-60')
    t.intersection_update('0-55')
    assert t == intspan('10-20,50-55')
    t.difference_update('16-20')
    assert t == intspan('10-15,50-55')
    t.symmetric_difference_update('10,99')
    assert t == intspan('11-15,50-55,99')


def test_pop():
    s = intspan('100-110')
    assert s.pop() == 100
    assert s.pop() == 101
    assert s.pop() == 102
    assert s.pop() == 103
    assert s.pop() == 104
    assert s.pop() == 105
    assert s == intspan('106-110')

    s = intspan('1-2')
    assert s.pop() == 1
    assert s.pop() == 2
    with pytest.raises(KeyError):
        s.pop()


def test_ranges():
    assert intspan().ranges() == []
    assert intspan('2').ranges() == [(2, 2)]
    assert intspan('1-3').ranges() == [(1, 3)]
    assert intspan('1-3,5-6').ranges() == [(1, 3), (5, 6)]


def test_from_range():
    assert intspan.from_range(1, 3) == intspan('1-3')
    assert intspan.from_range(2, 44) == intspan('2-44')


def test_from_ranges():
    assert intspan.from_ranges([(1, 3), (5, 6)]) == intspan('1-3,5-6')
    assert intspan.from_ranges([(1, 3)]) == intspan('1-3')
    assert intspan.from_ranges([(2, 2)]) == intspan('2')
    assert intspan.from_ranges([]) == intspan()


def test_universe():
    assert intspan().universe() == intspan()
    assert intspan('').universe() == intspan()
    assert intspan([]).universe() == intspan()

    assert intspan('1').universe() == intspan('1')

    assert intspan('1,3,5,7').universe() == intspan('1-7')

    s = intspan('1,3,5-9')
    assert s.universe() == intspan('1-9')
    assert s.universe(high=10) == intspan('1-10')
    assert s.universe(high=14) == intspan('1-14')
    assert s.universe(low=0) == intspan('0-9')
    assert s.universe(low=0, high=14) == intspan('0-14')
    assert s.universe(-2, 5) == intspan('-2-5')

    assert intspan('1-100').universe() == intspan('1-100')


def test_complement():
    s = intspan('1,3,5-9')
    assert s.complement() == intspan('2,4')
    assert s.complement(high=10) == intspan('2,4,10')
    assert s.complement(high=14) == intspan('2,4,10-14')
    assert s.complement(low=0) == intspan('0,2,4')
    assert s.complement(low=0, high=14) == intspan('0,2,4,10-14')

    assert s.complement(-2, 5) == intspan('-2,-1,0,2,4')

    items = intspan('1-3,5,7-9,10,21-24')
    assert items.complement() == intspan('4,6,11-20')
    assert items.complement(high=30) == intspan('4,6,11-20,25-30')

    with pytest.raises(ValueError):
        intspan().complement()
        # cannot get the complement of an empty set


def test_repr_and_str():
    s = intspan('10-20,50-55')
    s.add(9)
    s.discard('15-40')
    assert str(s) == '9-14,50-55'
    assert repr(s) == "intspan('" + str(s) + "')"
