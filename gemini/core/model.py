
from gemini.core.util import immutable

def tree(root):
    return immutable(root=root)

def migration(version, child, name):
    return immutable(
        version=version,
        child=child,
        name=name)
