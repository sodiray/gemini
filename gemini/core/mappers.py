
from gemini.core import model
from gemini.core.util import find

def _pop_obj(obj_list, condition):
    # Get the item that matches the condition
    obj = find(obj_list, condition)
    # Filter that item out - yes its more work/O but its
    # safer code/logic than altering the list in memory
    new_obj_list = [item for item in obj_list if not condition(item)]

    return obj, new_obj_list

def map_migration_to_node(migration_obj, child_migrations):
    version = migration_obj.get('version')
    name = migration_obj.get('name')
    child_migration_obj, remaining_migrations = _pop_obj(child_migrations, lambda m: m.get('parent') == version)

    if child_migration_obj is None:
        return model.migration(
            version=version,
            child=None,
            name=name)

    return model.migration(
        version=version,
        child=map_migration_to_node(child_migration_obj, remaining_migrations),
        name=name)

def map_migrations_to_tree(migrations):
    # Input:
    # [
    #     {
    #         'version': 'aaaaaaaaaa', # The Root/Initial migration
    #         'name': 'add_column',
    #         'parent': None  # we know because parent is none
    #     },
    #     {
    #         'version': 'bbbbbbbbbbb',
    #         'name': None,
    #         'parent': 'aaaaaaaaaa'
    #     },
    #     {
    #         'version': 'ccccccccc',
    #         'name': 'remove_stored_procedure',
    #         'parent': 'bbbbbbbbbbb'
    #     }
    # ]
    #
    # Output:
    # {
    #     version: 'aaaaaaaaaa'
    #     name: 'add_column',
    #     child: {
    #         version: 'bbbbbbbbbbb',
    #         name: None,
    #         child: {
    #             version: 'ccccccccc',
    #             name: 'remove_stored_procedure',
    #             child: None
    #         }
    #     }
    # }
    root_migration, child_migrations = _pop_obj(migrations, lambda m: m.get('parent') is None)

    if not root_migration:
        return model.tree(root=None)

    root_migration_node = map_migration_to_node(root_migration, child_migrations)

    return model.tree(root=root_migration_node)
