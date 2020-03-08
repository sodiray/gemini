from os import listdir
from os.path import isfile, join
from functools import reduce

from gemini.core.immutable import Immutable


def immutable(obj=None, **kwargs):
    if obj is not None:
        return Immutable(**obj)
    return Immutable(**kwargs)

def find(a_iterable, condition, default=None):
    return next((item for item in a_iterable if condition(item)), default)

def list_files(dir_path):
    return [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

def regex_find(string, pattern, default=None):
    res = pattern.search(string)
    if res is None:
        return None
    groups = res.groups()
    if groups is None or len(groups) < 1:
        return default
    return groups[0]

def template(string, key_value_dict):

    def reducer(acc, key_value):
        key = '{{%s}}' % key_value[0]
        value = key_value[1]
        return acc.replace(key, value or '')

    return reduce(reducer, key_value_dict.items(), string)


























# End
