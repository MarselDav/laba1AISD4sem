class Node:
    def __init__(self, byte_sequence, weight, left=None, right=None, parent=None):
        self.byte_sequence = byte_sequence
        self.weight = weight
        self.parent: Node = parent
        self.left: Node = left
        self.right: Node = right

    def updateWeights(self) -> int:
        if self.byte_sequence is not None:
            return self.weight
        else:
            w = 0
            if self.right is not None:
                w += self.right.updateWeights()
            if self.left is not None:
                w += self.left.updateWeights()
            self.weight = w
            return self.weight


class Tree:
    def __init__(self):
        self.esc = Node(None, 0)
        self.root = self.esc

    @staticmethod
    def getNodeCode(node: Node) -> str:
        code = ""
        parent: Node = node.parent
        while parent is not None:
            if parent.left == node:
                code += "0"
            else:
                code += "1"
            node = parent
            parent = node.parent
        return code[::-1]

    @staticmethod
    def update_parents_weights(node):
        while node is not None:
            node.weight += 1
            node = node.parent

    @staticmethod
    def swapNodes(first: Node, second: Node):
        first_parent = first.parent
        if first.parent == second.parent:
            if first.weight < second.weight:
                first_parent.left = first
                first_parent.right = second
            else:
                first_parent.left = second
                first_parent.right = first
        elif second.parent != first:
            if second.parent.left == second:
                second.parent.left = first
            else:
                second.parent.right = first

            first.parent = second.parent

            if first_parent.left == first:
                first_parent.left = second
            else:
                first_parent.right = second
            second.parent = first_parent

    def ESCAPE_NODE(self) -> Node:
        return self.esc

    def ROOT(self) -> Node:
        return self.root
