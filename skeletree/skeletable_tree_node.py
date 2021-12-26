"""Module that defines a generic tree node with payloads on leafs."""


from skeletree.sized_tree_node import SizedTreeNode
from skeletree.skeleton_leaf_node import SkeletonLeafNode
from skeletree.skeleton_resolved_inner_node import SkeletonResolvedInnerNode

# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class SkeletableTreeNode(SizedTreeNode):
    """Node of a generic (non-binary) tree with payloads on leafs.

    Size is computed lazily.
    """

    # Inherited constructor.

    # TODO: str and repr.

    def skeletize(self):
        """Return skeleton of this subtree.

        It is recommended to intern the result if only topology matters.
        """
        return SkeletonResolvedNode(subtree.skeletize() for subtree in self)
