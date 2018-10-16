def remove_brackets(word):
    return_word = word
    if word[0] == "(":
        return_word = return_word[1::]
    if word[-len(word)] == ")":
        return_word = return_word[::-1]
    return return_word


class Node:
    text: str
    type: str
    children: list = []
    parent = None
    return_type = ""

    def add_child(self, child):
        self.children.append(child)

    def is_compatible_with(self, right):
        right__type_split = right.type.rsplit("\\", 1)
        expected_left_type = right__type_split[0]
        if self.type == expected_left_type:
            self.return_type = remove_brackets(right__type_split[1])
            return True
        left__type_split = self.type.rsplit("/", 1)
        if len(left__type_split) == 2:
            expected_right_type = left__type_split[1]
            if right.type == expected_right_type:
                self.return_type = remove_brackets(expected_right_type[0])
                return True
        return False

    def print(self):
        print(self.type + "\n")
        print(self.text + "\n")
        for child in self.children:
            child.print()


rules = {
    'i': "np",
    "want": "(np\s)/np",
    "a": "np/np",
    "restaurant": "np",
    "serving": "(s\s)/np",
    "swedish": "np/np",
    "food": "np"
}
variable_types = {
    "area": {
        "keywords": ["town", "of"],
        "words": ["east", "west", "north", "south", "centre"]
    },
    "price_range": {
        "keywords": ["restaurant", "price"],
        "words": ["moderate", "expensive", "cheap"]
    },
    "food": {
        "keywords": ["restaurant", "serves", "serving", "food"],
        "words": ["thai", "turkish", "european", "catalan", "mediterranean", "seafood", "british", "modern european", "italian", "romanian", "chinese", "steakhouse", "asian oriental", "french", "portuguese", "indian", "spanish", "vietnamese", "korean", "moroccan", "swiss", "fusion", "gastropub", "tuscun", "international", "traditional", "mediterranean", "poynesian", "african", "turkish", "bistro", "north american", "australasian", "persian", "jamaican", "lebanese", "cubun", "japenese", "catalan"]
    }
}
variable_nodes = dict()


def evaluate_word_list(nodes: list) -> Node:
    tree_node = Node()
    new_nodes = list()
    i = 0
    for node in nodes:
        if i != len(nodes):
            if node.is_compatible_with(nodes[i+1]):
                new_node = Node()
                new_node.type = node.return_type
                new_node.text = node.text + " " + nodes[i+1].text
                new_node.children.append(node)
                new_node.children.append(nodes[i+1])
                node.parent = new_node
                nodes[i+1].parent = new_node
                new_nodes.append(new_node)
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
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
        if word in rules.keys():
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
    for variable_type, v_value in variable_types.items():
        for word in word_list:
            if word in v_value["keywords"]:
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
    print("\n---------\n")
    print("VARIABLES\n")
    print("---------\n")
    print("---------")
    for key, value in variable_nodes.items():
        print("---------\n")
        print(key + "\n")
        value.print()
