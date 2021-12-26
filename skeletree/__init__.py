
"""Sekeletable resolved tree.

Treemeans there are leaf nodes and inner nodes.
Leaf nodes may carry a single payload.
Inner nodes may have one or more children.
The payloads are only in leafnodes.
Skeletable means it is possible to extract a skeleton.
Skeleton is a tree with the sametopology but no payloads.
Size of a subtree is the number of its leaves.
If two children of a node have the same size, the node is unresolved.
Resonved node cannot have topologically identical children,
and for soreting order of children does not matter,
so children can be stored in frozenset, and resolved skeletons are hashable,
so we can intern them.
"""