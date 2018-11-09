from node import Node
import copy


class SentenceTreeBuilder:

    def build_tree(self, nodes: list) -> Node:
        new_nodes = list()
        new_nodes.append([[], []])

        def node_can_be_appended(n: list, n_nodes: list):
            for used_node in n[1]:
                for node_to_be_appended in n_nodes:
                    if used_node.text == node_to_be_appended.text:
                        return False
            return True

        def append_unchanged_node(n: Node):
            j = 0
            for n_nodes in new_nodes:
                if node_can_be_appended(n_nodes, [n]):
                    new_nodes[j][0].append(n)
                    new_nodes[j][1].append(n)
                j += 1

        def create_new_node(left_node, right_node) -> Node:
            n_node = Node()
            n_node.children = []
            n_node.types = [left_node.return_type]
            n_node.type = left_node.return_type
            n_node.text = left_node.text + " " + right_node.text
            n_node.children.append(left_node)
            n_node.children.append(right_node)
            left_node.parent = n_node
            right_node.parent = n_node
            return n_node

        def create_new_nodes_lists(n_node: Node, left_node, right_node):
            length = len(new_nodes)
            for j in range(0, length):
                if node_can_be_appended(new_nodes[j], [left_node, right_node]):
                    n_nodes_with_change = copy.deepcopy(new_nodes[j])
                    n_nodes_with_change[0].append(n_node)
                    n_nodes_with_change[1].append(left_node)
                    n_nodes_with_change[1].append(right_node)
                    new_nodes.append(n_nodes_with_change)
                    new_nodes[j][0].append(left_node)
                    new_nodes[j][1].append(left_node)

        def remove_original_list_from_new_nodes():
            new_nodes.pop(0)

        def attempt_all_trees() -> Node:
            attempted_root_node = get_root_node()
            if attempted_root_node.text != "":
                return attempted_root_node
            for n_nodes in new_nodes:
                next_recursive_iteration_result = self.build_tree(n_nodes[0])
                if next_recursive_iteration_result.text != "":
                    return next_recursive_iteration_result
            return Node()

        def get_root_node() -> Node:
            for n_nodes in new_nodes:
                new_nodes_nodes = n_nodes[0]
                if len(new_nodes_nodes) == 1:
                    return new_nodes_nodes[0]
            return Node()

        nodes_length = len(nodes)
        for i in range(0, nodes_length):
            node = nodes[i]
            if i < len(nodes) - 1:
                r_node = nodes[i + 1]
                if node.is_compatible_with(r_node):
                    new_node = create_new_node(node, r_node)
                    create_new_nodes_lists(new_node, node, r_node)
                else:
                    append_unchanged_node(node)
            else:
                append_unchanged_node(node)
        remove_original_list_from_new_nodes()
        return attempt_all_trees()
