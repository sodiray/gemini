import pytest

from gemini.core import util


def test_find_finds_object():

    ray = util.immutable(name='ray', roles=['a', 'b'])
    joe = util.immutable(name='joe', roles=['x'])
    carl = util.immutable(name='carl', roles=['a'])

    user_list = [ ray, joe, carl ]

    assert util.find(user_list, lambda u: u.name == 'ray') == ray
    assert util.find(user_list, lambda u: 'x' in u.roles) == joe
    assert util.find(user_list, lambda u: 'NOPE' in u.roles) == None
    assert util.find(user_list, lambda u: 'NOPE' in u.roles, 'mydefault') == 'mydefault'
