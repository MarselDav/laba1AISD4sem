from source.AdaptiveHaffmanCoding.HaffmanTree import Node


class ReorderingTreeMethods:
    def __init__(self, sequence_len):
        self.sequence_len = sequence_len

    @staticmethod
    def reorder_nodes(nodeList):
        i = 1
        while i < len(nodeList):
            if nodeList[i - 1].weight < nodeList[i].weight:
                break
            i += 1
        if i != len(nodeList):
            first = nodeList[i]
            j = 0
            while j < i:
                if nodeList[j].weight < first.weight:
                    break
                j += 1
            # swapNodes
            first_parent = first.parent
            second = nodeList[j]
            if first.parent == second.parent:
                if first.weight < second.weight:
                    first_parent.left = first
                    first_parent.right = second
                else:
                    first_parent.left = second
                    first_parent.right = first
            else:
                if second.parent != first:
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
            nodeList[j] = first
            nodeList[i] = second
            return True
        return False

    def update_by_character(self, byte_sequence, nodeCash, tree, nodeList):
        code = str()
        dec_num_byte = int.from_bytes(byte_sequence, byteorder="big")
        node = nodeCash[dec_num_byte]
        if node is not None:
            node.weight += 1
            parent = node.parent

            code += tree.getNodeCode(node)
        else:
            esc_code = tree.getNodeCode(tree.ESCAPE_NODE())

            code += esc_code
            code += bin(dec_num_byte)[2::].rjust(8 * self.sequence_len, "0")

            zero_node_parent = tree.ESCAPE_NODE().parent
            new_node = Node(byte_sequence, 1)
            intermediate = Node(None, 0, tree.ESCAPE_NODE(), new_node, zero_node_parent)
            nodeCash[dec_num_byte] = new_node
            new_node.parent = intermediate
            if zero_node_parent is not None:
                zero_node_parent.left = intermediate
            else:
                tree.root = intermediate
            nodeList[-1] = intermediate
            nodeList.append(new_node)
            nodeList.append(tree.ESCAPE_NODE())
            tree.ESCAPE_NODE().parent = intermediate
            parent = new_node.parent

        while parent is not None:
            parent.weight += 1
            parent = parent.parent

        while self.reorder_nodes(nodeList):
            tree.ROOT().updateWeights()

        # print(code, end="")
        return code
