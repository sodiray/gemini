import uuid

from gemini.core.mappers import map_migrations_to_tree
from gemini.core.tree import get_last_migration
from gemini.runtimes.util import find_runtime, detect_runtime


def run(runtime_key=None, message=None):

    if runtime_key is None:
        runtime_key = detect_runtime()
    runtime = find_runtime(runtime_key)

    migrations = runtime.get_migrations()

    migration_tree = map_migrations_to_tree(migrations)
    last_migration = get_last_migration(migration_tree)

    is_root = last_migration is None

    new_version = make_migration_id()
    parent = None if is_root else last_migration.version

    file_message = format_migration_message(message)

    runtime.create_migration(
        new_version=new_version,
        parent=parent,
        name=file_message)

def format_migration_message(message):
    if message is None:
        return ''
    return message.lower().replace(' ', '_')

def make_migration_id():
    id = uuid.uuid4().hex[:7]
    # Prepending g so all migrations start with a letter
    # to bypass importing and dynamic file loading issues
    return f'g{id}'
