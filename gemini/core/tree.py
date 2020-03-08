


def get_last_migration(tree):
    def get_last_child(migration):
        if migration.child is None:
            return migration
        return get_last_child(migration.child)
    if tree.root is None:
        return None
    return get_last_child(tree.root)

def traverse_tree(tree, start_node=None):
    start_node = tree.root if start_node is None else start_node
    for node in iter_nodes(start_node):
        yield node

def iter_nodes(start_node):
    yield start_node
    if start_node.child:
        yield from iter_nodes(start_node.child)

def find_node(node, condition):
    for node in iter_nodes(node):
        if condition(node):
            return node
