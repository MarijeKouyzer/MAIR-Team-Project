class Node:
    text: str
    type: str
    children: list = []
    parent = None

    def add_child(self, child):
        self.children.append(child)

    def is_compatible_with(self, right):
        right__type_split = right.type.split("\\")
        expected_left_type = right__type_split[-len(right__type_split)]
        if self.type == expected_left_type:
            return True
        left__type_split = self.type.split("/")
        expected_right_type = left__type_split[-len(left__type_split)]
        if right.type == expected_right_type:
            return True
        return False

    @property
    def return_type(self) -> str:
        i = 0
        for c in reversed(self.type):
            if c == "/" or c == "\\":
                return self.type[::-i]
            i += 1
        return ""

    def print(self):
        print(self.type + "\n")
        print(self.text + "\n")
        for child in self.children:
            child.print()


rules = {

}
variable_nodes = dict()
variable_types = {
    "area": {
        "keywords": ["town", "of"],
        "words": ["east", "west", "north", "south"]
    },
    "price_range": {
        "keywords": ["restaurant"],
        "words": []
    }
}


def evaluate_word_list(nodes: list) -> Node:
    tree_node = Node()
    new_nodes = list()
    i = 0
    for node in nodes:
        if nodes[i+1] and node.is_compatible_with(nodes[i+1]):
            new_node = Node()
            new_node.type = node.return_type
            new_node.text = node.text + " " + node[i+1].text
            new_node.children.append(node)
            new_node.children.append(nodes[i+1])
            node.parent = new_node
            node[i+1].parent = new_node
            new_nodes.append(new_node)
        i += 1
    tree_is_complete = len(new_nodes) == 1
    if tree_is_complete:
        tree_node = new_nodes[0]
    nothing_changed = True
    if nothing_changed or tree_is_complete:
        return tree_node
    return Node()


def build_tree(text: str) -> Node:
    # Change the text into a list of nodes containing the word and the type
    word_list = text.split(" ")
    node_list = list()
    for word in word_list:
        word_node = Node()
        word_node.text = word
        if rules[word]:
            word_node.type = rules[word]
        else:
            word_node.type = "np"
        node_list.append(word_node)
    # Return the tree
    return evaluate_word_list(node_list)


def find_variables_in_branch(node, variable_type):
    # Node is a leaf
    if len(node.children) == 0:
        if node.text in variable_types[variable_type]["words"]:
            variable_nodes[variable_type] = node
    # If not, continue to the children
    else:
        for child in node.children:
            find_variables_in_branch(child, variable_type)


def traverse_tree(node):
    # See if there are multiple variable types in the sub(tree)
    variable_types_in_text = list()
    word_list = node.text.split(" ")
    for variable_type, value in variable_types.items():
        for word in word_list:
            if word in value["keywords"]:
                variable_types_in_text.append(variable_types)
    if len(variable_types_in_text) == 1:
        # The node is a node containing a single type of variable
        find_variables_in_branch(node, variable_types_in_text[0])
        return
    # Make sure we don't traverse when not necessary
    if len(variable_types_in_text) == 0:
        return
    for child in node.children:
        traverse_tree(child)


# Wait for input
while True:
    user_text = input("Enter text to evaluate: ")
    root_node = build_tree(user_text)
    variable_nodes = dict()
    traverse_tree(root_node)
    root_node.print()
    print("\nVARIABLES\n")
    print("---------\n")
    print("---------")
    for key, value in variable_nodes.items():
        print("---------\n")
        print(key + "\n")
        value.print()
