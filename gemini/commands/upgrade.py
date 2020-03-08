from gemini.core.mappers import map_migrations_to_tree
from gemini.core.tree import get_last_migration, traverse_tree, find_node
from gemini.runtimes.util import get_current_runtime


def run():
    runtime = get_current_runtime()

    version = runtime.get_database_version()
    migrations = runtime.get_migrations()

    migration_tree = map_migrations_to_tree(migrations)

    if migration_tree.root is None:
        raise Exception('Could not find any migrations to run')

    start_node = get_start_node(version, migration_tree)

    if start_node is None:
        return

    for migration in traverse_tree(migration_tree, start_node=start_node):
        print(f'Running migration: {migration.name}')
        runtime.run_up(migration.version)

def get_start_node(version, tree):

    if version is None:
        print('Fresh database, running all migrations')
        return tree.root

    current_version_node = find_node(tree.root, lambda node: node.version == version)

    if current_version_node.child is None:
        print('Database is already up to date')
        return None

    return current_version_node.child
