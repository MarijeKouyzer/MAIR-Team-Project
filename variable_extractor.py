class VariableExtractor:

    variable_types = {
        "area": {
            "keywords": ["town", "of", "in"],
            "words": ["east", "west", "north", "south", "center", "centre", "any"]
        },
        "price_range": {
            "keywords": ["restaurant", "price"],
            "words": ["moderate", "expensive", "cheap", "moderately"]
        },
        "food": {
            "keywords": ["restaurant", "serves", "serving", "food"],
            "words": ["swedish",
                      "thai",
                      "turkish",
                      "european",
                      "catalan",
                      "mediterranean",
                      "seafood",
                      "british",
                      "modern european",
                      "italian",
                      "romanian",
                      "chinese",
                      "steakhouse",
                      "asian oriental",
                      "french",
                      "portuguese",
                      "indian",
                      "spanish",
                      "vietnamese",
                      "korean",
                      "moroccan",
                      "swiss",
                      "fusion",
                      "gastropub",
                      "tuscan",
                      "international",
                      "traditional",
                      "mediterranean",
                      "poynesian",
                      "african",
                      "turkish",
                      "bistro",
                      "north american",
                      "australasian",
                      "persian",
                      "jamaican",
                      "lebanese",
                      "cuban",
                      "japenese",
                      "catalan",
                      "world"]
        }
    }
    variable_nodes = dict()

    def __init__(self):
        self.variable_nodes = dict()

    def find_variables_in_branch(self, node, variable_type: str):
        if node.text in self.variable_types[variable_type]["words"]:
            node.variable_type = variable_type
            self.variable_nodes[variable_type] = node
            return
        if len(node.children) != 0:
            for child in node.children:
                self.find_variables_in_branch(child, variable_type)

    def search_for_variables_in_tree(self, tree):
        for var_type in self.variable_types.keys():
            if var_type not in self.variable_nodes.keys():
                self.find_variables_in_branch(tree, var_type)

    def search_for_variable_without_tree(self, nodes: list):
        for node in nodes:
            for var_type in self.variable_types.keys():
                if var_type not in self.variable_nodes.keys():
                    self.find_variables_in_branch(node, var_type)

    def traverse_tree(self, node):
        # See if there are multiple variable types in the sub(tree)
        variable_types_in_text = list()
        word_list = node.text.split(" ")
        for variable_type, v_value in self.variable_types.items():
            for word in word_list:
                if word in v_value["keywords"]:
                    variable_types_in_text.append(variable_type)
        if len(variable_types_in_text) == 1:
            # The node is a node containing a single type of variable
            self.find_variables_in_branch(node, variable_types_in_text[0])
            return
        # Make sure we don't traverse when not necessary
        if len(variable_types_in_text) == 0:
            return
        for child in node.children:
            self.traverse_tree(child)
