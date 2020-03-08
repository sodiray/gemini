import re
import os
from os.path import splitext

from gemini.core.util import list_files

from gemini.runtimes.python import runtime as python_runtime
from gemini.runtimes.csharp import runtime as csharp_runtime


migration_filename_pattern = re.compile("([a-z0-9]){8}\_([a-z_]+)?\.(py|csx)")

runtime_map = {
    'py': python_runtime,
    'csx': csharp_runtime
}


def is_migration_file(file_name):
    return migration_filename_pattern.match(file_name) is not None

def list_migration_files(dir_path='./migrations'):
    file_names = os.listdir(dir_path)
    return list(filter(lambda f: is_migration_file(f), file_names))

def read_migration_files(migration_dir='./migrations'):
    file_names = list_migration_files(migration_dir)
    relative_file_names = map(lambda f: os.path.join(migration_dir, f), file_names)
    return list(map(lambda f: open(f, 'r').read(), relative_file_names))

def find_runtime(key):

    runtime = runtime_map.get(key, None)
    if runtime is None:
        raise Exception(f'Provided language runtime key is not recognized: {key}')
    return runtime

def detect_runtime():

    migration_files = list_files('./migrations')

    if len(migration_files) < 1:
        raise Exception('No files in migrations directory to use as clue for language runtime')

    file_name = migration_files[0]
    _, file_ext = splitext(file_name)
    ext = file_ext.replace('.', '')

    if ext not in runtime_map:
        raise Exception(f'Migration file extension types are not supported: {ext}')

    return ext

get_current_runtime = lambda: find_runtime(detect_runtime())
