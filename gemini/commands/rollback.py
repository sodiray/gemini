from gemini.core.mappers import map_migrations_to_tree
from gemini.core.tree import get_last_migration
from gemini.runtimes.util import get_current_runtime


def run():

    runtime = get_current_runtime()

    version = runtime.get_database_version()

    migrations = runtime.get_migrations()

    migration_tree = map_migrations_to_tree(migrations)
    last_migration = get_last_migration(migration_tree)

    if last_migration.version != version:
        raise Exception('The current version of the data source is out of sync')

    print(f'Rolling back migration: {last_migration.name}')
    runtime.run_down(last_migration.version)
