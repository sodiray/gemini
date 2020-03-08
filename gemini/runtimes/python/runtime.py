import uuid
import sys
import os
import re
import importlib.util

from gemini.core.util import template, find, regex_find
from gemini.runtimes import util

# A runtime is simply a wrapper/translation service to abstract away
# language specific migration code. For the most part, functions in
# this runtime (and all others) should be kept simple and only be made
# to return data from the users migrations directory given the user is
# using a python gemini setup.

version_pattern = re.compile("version = \'([a-z0-9]{8}|root)\'")
parent_pattern = re.compile("parent = \'([a-z0-9]{8})\'")
name_pattern = re.compile("name = \'(.+)\'")

def get_database_version():
    curr_dir_path = os.getcwd()
    sys.path.insert(1, curr_dir_path)
    from geminiver import get_database_version
    return get_database_version()

def set_database_version(version):
    curr_dir_path = os.getcwd()
    sys.path.insert(1, curr_dir_path)
    from geminiver import set_database_version
    return set_database_version(version)

def get_migrations():
    # read all files from ./migrations directory
    # filter out files that don't match [a-z]*8_([a-zA-Z_]+)?\.py pattern
    # go through the files found and read each version and parent version
    # return whatcha found yo

    migration_files = util.read_migration_files('./migrations')

    def map_script_to_migration_obj(script):
        return {
            'version': regex_find(script, version_pattern),
            'parent': regex_find(script, parent_pattern),
            'name': regex_find(script, name_pattern)
        }

    return list(map(map_script_to_migration_obj, migration_files))

def run_down(migration_version):
    # find the migration file for the given id
    # run the down method in the file
    migration = _find_migration_module_for_version(migration_version)
    migration.down()

def run_up(migration_version):
    # find the migration file for the given id
    # run the up method in the file
    migration = _find_migration_module_for_version(migration_version)
    migration.up()

def create_migration(new_version, parent, name):
    # create a new file in the migrations directory
    # that is a template for the current runtime and version

    template_str = '''

version = '{{new_version}}'
parent = {{parent}}
name = '{{name}}'

def up():
    pass


def down():
    pass

    '''

    file_content = template(template_str, {
        'new_version': new_version,
        'parent': 'None' if parent is None else f"'{parent}'",
        'name': name
    })

    file_name = f'{new_version}_{name}.py'

    curr_dir_path = os.getcwd()
    file_location = os.path.join(curr_dir_path, 'migrations', file_name)

    with open(file_location, "w") as file:
        file.write(file_content)

def setup():
    # Run whatever script needed to install csharp specific runtime
    # dependencies - dotnet-script, dotnet, etc.
    print('Done - all python requirements are satisfied. No setup work to do.')

def _find_migration_module_for_version(version):

    file_names = util.list_migration_files('./migrations')
    file_name = find(file_names, lambda name: version in name)
    file_path = os.path.join('./migrations', file_name)

    spec = importlib.util.spec_from_file_location(f'migrations.{version}', file_path)
    migration_module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(migration_module)

    return migration_module
