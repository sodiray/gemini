import pytest

from gemini.core import mappers
from gemini.core import util


def test__pop_object_pops_objects():

    ray = util.immutable(name='ray', roles=['a', 'b'])
    joe = util.immutable(name='joe', roles=['x'])
    carl = util.immutable(name='carl', roles=['a'])

    user_list = [ ray, joe, carl ]

    user, remaining = mappers._pop_obj(user_list, lambda u: u.name == 'ray')

    assert user == ray
    assert ray not in remaining
    assert joe in remaining
    assert carl in remaining

def test_map_migrations_to_tree():
    pass
