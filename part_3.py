import copy
import re
from Levenshtein.StringMatcher import StringMatcher as sm


def remove_brackets(word):
    return_word = word
    print("in remove brackets ", return_word)
    if return_word[0] == "(":
        return_word = return_word[1::]
    if return_word[(len(return_word) - 1)] == ")":
        return_word = return_word[:-1]
    print(return_word, " is returned")
    return return_word


class Node:
    text: str = ""
    type: str = ""
    types: list = []

    children: list = []
    parent = None
    return_type = ""
    # 0 or 1
    return_rule = 1

    def add_child(self, child):
        self.children.append(child)

    def is_compatible_with(self, right):
        print("*******************")
        print("left  text:", self.text)
        print("      types:", self.types)
        print("right text", right.text)
        print("      types:", right.types)
        print("*******************")
        for left_type in self.types:
            for right_type in right.types:
                right__type_split = right_type.rsplit("\\", 1)
                if len(right__type_split) == 2:
                    expected_left_type = right__type_split[0]
                    print("expected: " + expected_left_type + ", actual: " + left_type)
                    if left_type == remove_brackets(expected_left_type):
                        self.type = left_type
                        right.type = right_type
                        self.return_type = remove_brackets(right__type_split[1])
                        self.return_rule = 0
                        return True

                left__type_split = left_type.rsplit("/", 1)
                if len(left__type_split) == 2:
                    expected_right_type = left__type_split[1]
                    print("expected: " + expected_right_type + ", actual: " + right_type)
                    if right_type == remove_brackets(expected_right_type):
                        self.type = left_type
                        right.type = right_type
                        self.return_type = remove_brackets(left__type_split[0])
                        self.return_rule = 1
                        return True
        return False

    def print(self):
        print("type: " + self.type)
        print("text: " + self.text)
        print("<children>")
        for child in self.children:
            child.print()
            print("---------")
        print("</children>")

    def variable_print(self):
        if self.parent:
            self.parent.variable_print()
        print("type: " + self.type)
        print("text: " + self.text)
        print("--------")


rules = {
    "i": ["np"],
    "want": ["np\s/np"],
    "a": ["np/n"],
    #"restaurant": ["n"],<- original
    "restaurant": ["n", "(s/pp\(s))/(n\\s\\s)"],
    "serving": ["s\s/n"],
    "swedish": ["n/n"],
    "about": ["n\s/n"],
    "an": ["np\s/n", "np/n"],
    "and": ["(s\s)/s", "(np\np)/np"],
    "any": ["np", "np/np"],
    "area": ["np"],
    "can": ["np/np"],
    "catalan": ["n/n"],
    "center": ["n"],
    "cheap": ["n/n"],
    "chinese": ["n/n"],
    "cuban": ["n/n"],
    "expensive": ["n/n"],
    "find": ["np/np", "np\s/np", "np\s/pp/np"],
    #"for": ["pp/np", "pp/n"], <- origin rule
    "for": ["pp/np", "pp/n", "(s/pp/pp)\((np)/(np\np))/(np\s)"],
    "have": ["np\s/np\s"],
    "im": ["np"],
    "in": ["pp/np", "n\pp/np"],
    "international": ["n/n"],
    "is": ["n/n", "n\s/pp/np"],
    "it": ["np"],
    "serve": ["(np\s)/n"],
    "serves": ["s/n"],
    "should": ["(np\s)/(np\s)"],
    "like": ["(np\s)/pp/np"],
    "looking": ["np\s/pp/pp", "np\s/pp"],
    "moderately": ["n/n"],
    "need": ["np\s/np", "np"],
    "of": ["pp/np"],
    "part": ["n/pp"],
    "persian": ["n/n"],
    "please": ["s\s", "pp"],
    "priced": ["n/pp", "n"],
    "south": ["n/n"],
    "that": ["s\s/s", "s\s/n"],
    "the": ["np/n"],
    "town": ["np"],
    "tuscan": ["n/n"],
    "wanna": ["np\s/np"],
    "west": ["n/n"],
    "what": ["n"],
    "with": ["n\s\s/n"],
    "world": ["n/n"],
    "would": ["np\s/(np\s)"],
    "address": ["np"],
    "afghan": ["np/np"],
    "african": ["np/np"],
    "again": ["v\\vp"],
    "ah": ["s/s"],
    "alright": ["s/s"],
    "am": ["(np\s)/np", "(np\s)/(np\s)"],
    "american": ["np/np"],
    "anyone": ["np"],
    "anything": ["np"],
    "fancy": ["np/np"],
    "fast": ["np/np"],
    "fine": ["s/s"],
    "fish": ["np/np"],
    "food": ["n"],
    "foods": ["n"],
    "canapes": ["np/np"],
    "cantonese": ["np/np"],
    "care": ["np\s"],
    "caribbean": ["np/np"],
    "central": ["np", "np/np"],
    "centre": ["np"],
    "change": ["(np\s)/np", "(np\s)/(np\s)"],
    "iam": ["s"],
    "id": ["s"],
    "if": ["s/s"],
    "includes": ["(np\s)/np"],
    "indian": ["np/np"],
    "indonesian": ["np/np"],
    "inner": ["np/np"],
    "irish": ["np/np"],
    "italian": ["np/np"],
    "served": ["np\\np"],
    "list": ["np"],
    "long": ["np/np"],
    "look": ["(np\s)/(np\s)", "np\s"],
    "malaysian": ["np/np"],
    "matter": ["np\s"],
    "may": ["(np\s)/(np\s)"],
    "me": ["np"],
    "meant": ["np\s"],
    "mediterranean": ["np/np"],
    "medium": ["np/np"],
    "mexican": ["np/np"],
    "mind": ["np\s"],
    "missing": ["np/np", "np\s"],
    "moderate": ["np/np"],
    "modern": ["np/np"],
    "moroccan": ["np/np"],
    "moron": ["np"],
    "music": ["np"],
    "my": ["np/np"],
    "needs": ["np", "np\s/np"],
    "no": ["np/np"],
    "north": ["np/np"],
    "not": ["np/np", "np"],
    "parts": ["n/pp"],
    "place": ["np"],
    "polish": ["np/np"],
    "polynesia": ["np/np"],
    "polynesian": ["np/np"],
    "portuguese": ["np/np"],
    "prezzo": ["np"],
    "price": ["np", "np/np"],
    "prices": ["np"],
    "range": ["np"],
    "really": ["np/np"],
    "reasonably": ["np/np"],
    "repeat": ["np\s"],
    "type": ["np"],
    "uh": ["s/s", "s\s", "np\\np", "np/np"],
    "um": ["s/s", "s\s", "np\\np", "np/np"],
    "umh": ["s/s", "s\s", "np\\np", "np/np"],
    "unusual": ["np/np"],
    "vegetarian": ["np/np"],
    "venetian": ["np/np"],
    "venue": ["np"],
    "venues": ["np"],
    "vietnam": ["np/np"],
    "vietnamese": ["np/np"],
    "spanish": ["np/np"],
    "steak": ["np/np", "np"],
    "steakhouse": ["np/np", "np"],
    "such": ["np/np"],
    "surprise": ["(np\s)/np"],
    "swiss": ["np/np"],
    "system": ["s/s", "s\s", "np\\np", "np/np"],
    "tell": ["(np\s)/np"],
    "thai": ["np/np"],
    "thailand": ["np/np"],
    "thats": ["s"],
    "their": ["np/np"],
    "then": ["s/s", "s\s", "np\\np", "np/np"],
    "there": ["np"],
    "theres": ["s"],
    "they": ["np"],
    "thing": ["np"],
    "this": ["np/np"],
    "time": ["np"],
    "to": ["pp/np"],
    "traditional": ["np/np"],
    "try": ["(np\s)/np"],
    "trying": ["(np\s)/np"],
    "turkey": ["np/np"],
    "turkish": ["np/np"],
    "was": ["vp/adjP", "np\((s/pp)/np)"],
    "well": ["s/s", "s\s"],
    "welsh": ["np/np"],
    "whats": ["s"],
    "anywhere": ["np"],
    "are": ["(np\s)/np", "(np\s)/(np\s)"],
    "areas": ["np"],
    "asian": ["np/np"],
    "at": ["pp/np"],
    "australasian": ["np/np"],
    "australian": ["np/np"],
    "austrian": ["np/np"],
    "available": ["np/np", "adjP"],
    "barbecue": ["np/np"],
    "basque": ["np/np"],
    "be": ["(np\s)/(np\s)"],
    "belgian": ["np/np"],
    "belgium": ["np/np"],
    "beside": ["(s\s)/s"],
    "bistro": ["np/np"],
    "brazilian": ["np/np"],
    "breath": ["s/s", "s\s"],
    "british": ["np/np"],
    "but": ["(s\s)/s"],
    "bye": ["s"],
    "cambridge": ["np/np"],
    "chiquito": ["np/np"],
    "christmas": ["np/np"],
    "city": ["np/np", "np\\np"],
    "class": ["np"],
    "corsica": ["np/np"],
    "could": ["s/(np\s)"],
    "creative": ["np/np"],
    "crossover": ["np/np"],
    "damn": ["np/np"],
    "danish": ["np/np"],
    "dear": ["np/np"],
    "decide": ["(np\s)/np"],
    "did": ["(np\s)/np", "(np\s)/(np\s)"],
    "different": ["np/np"],
    "do": ["(np\s)/np", "(np\s)/(np\s)"],
    "does": ["(np\s)/np", "(np\s)/(np\s)"],
    "doesnt": ["(np\s)/np", "(np\s)/(np\s)"],
    "dont": ["(np\s)/np", "(np\s)/(np\s)"],
    "downtown": ["np/np"],
    "east": ["np/np"],
    "eat": ["(np\s)/np"],
    "else": ["s\s"],
    "english": ["np/np"],
    "eritrean": ["np/np"],
    "european": ["np/np"],
    "every": ["np/np"],
    "french": ["np/np"],
    "from": ["pp/np"],
    "fusion": ["np/np"],
    "gastro": ["np/np"],
    "gastropub": ["np/np"],
    "german": ["np/np"],
    "get": ["(np\s)/np"],
    "give": ["(np\s)/np"],
    "good": ["np/np"],
    "got": ["(np\s)/np"],
    "greek": ["np/np"],
    "halal": ["np/np"],
    "harbor": ["np/np"],
    "has": ["(np\s)/np", "(np\s)/(np\s)"],
    "help": ["np/s"],
    "high": ["np/np"],
    "hindi": ["np/np"],
    "house": ["np"],
    "how": ["pp/np"],
    "hungarian": ["np/np"],
    "its": ["np/np"],
    "jamaican": ["np/np"],
    "japanese": ["np/np"],
    "just": ["s\s", "s/s"],
    "kind": ["np/np"],
    "know": ["(np\s)/np"],
    "korea": ["np/np"],
    "korean": ["np/np"],
    "kosher": ["np/np"],
    "lebanese": ["np/np"],
    "let": ["s/s"],
    "lets": ["s/s"],
    "oh": ["s/s"],
    "ok": ["s/s", "np/np"],
    "okay": ["s/s"],
    "on": ["pp/np"],
    "one": ["np/np"],
    "oriental": ["np/np"],
    "other": ["np/np"],
    "pan": ["np"],
    "park": ["np"],
    "restaurants": ["n"],
    "rice": ["np"],
    "romania": ["np/np"],
    "romanian": ["np/np"],
    "russian": ["np/np"],
    "said": ["np\s"],
    "says": ["np\s"],
    "scandinavia": ["np/np"],
    "scandinavian": ["np/np"],
    "scottish": ["np/np"],
    "sea": ["np"],
    "seafood": ["np"],
    "searching": ["(np\s)/np"],
    "see": ["(np\s)/np"],
    "sells": ["(np\s)/np"],
    "side": ["np"],
    "singapore": ["np/np"],
    "singaporean": ["np/np"],
    "so": ["s/s", "s\s", "np\\np", "np/np"],
    "sock": ["np"],
    "some": ["np/np"],
    "something": ["np"],
    "sorry": ["s", "s/s", "s\s"],
    "yes": ["s/s", "s\s"],
    "you": ["np"],
    "yourself": ["np"]
}

variable_types = {
    "area": {
        "keywords": ["town", "of", "in"],
        "words": ["east", "west", "north", "south", "center", "centre"]
    },
    "price_range": {
        "keywords": ["restaurant", "price"],
        "words": ["moderate", "expensive", "cheap"]
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
                  "tuscun",
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


def build_tree(nodes: list) -> Node:
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
            next_recursive_iteration_result = build_tree(n_nodes[0])
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


def get_word(word):
    if word in rules.keys():
        return word, rules[word]
    levenshtein_distances = {}
    for word_key in rules.keys():
        levenshtein_distances[word_key] = sm(seq1=word, seq2=word_key).distance()
    min_valued_word = ""
    min_valued_word_value = -1
    for k_key, v_value in levenshtein_distances.items():
        if v_value < min_valued_word_value or min_valued_word_value == -1:
            min_valued_word = k_key
            min_valued_word_value = v_value
    return min_valued_word, rules[min_valued_word]


def build_node_list(line: str) -> list:
    # Change the text into a list of nodes containing the word and the type
    word_list = line.split(" ")
    node_list = list()
    for word in word_list:
        word_node = Node()
        word, types = get_word(word)
        word_node.text = word
        word_node.types = types
        node_list.append(word_node)
    # Return the nodes
    return node_list


def find_variables_in_branch(node, variable_type: str):
    if node.text in variable_types[variable_type]["words"]:
        node.variable_type = variable_type
        variable_nodes[variable_type] = node
        return
    if len(node.children) != 0:
        for child in node.children:
            find_variables_in_branch(child, variable_type)


def traverse_tree(node):
    # See if there are multiple variable types in the sub(tree)
    variable_types_in_text = list()
    word_list = node.text.split(" ")
    for variable_type, v_value in variable_types.items():
        for word in word_list:
            if word in v_value["keywords"]:
                variable_types_in_text.append(variable_type)
    if len(variable_types_in_text) == 1:
        # The node is a node containing a single type of variable
        find_variables_in_branch(node, variable_types_in_text[0])
        return
    # Make sure we don't traverse when not necessary
    if len(variable_types_in_text) == 0:
        return
    for child in node.children:
        traverse_tree(child)


def normalise_line(line):
    # Make text lower case
    text = line.lower()
    # Remove characters from string to standardise the strings
    text = re.sub('[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '', text)
    return text


def search_for_variables_in_tree(tree):
    for var_type in variable_types.keys():
        if var_type not in variable_nodes.keys():
            find_variables_in_branch(tree, var_type)


def search_for_variable_without_tree(nodes: list):
    for node in nodes:
        for var_type in variable_types.keys():
            if var_type not in variable_nodes.keys():
                find_variables_in_branch(node, var_type)


# Wait for input

while True:
    user_text = input("Enter text to evaluate: ")
    nodes_list = build_node_list(normalise_line(user_text))
    root_node = build_tree(nodes_list)
    variable_nodes = dict()
    print("The root node will be ", root_node.text)
    print("TREE")
    print("--------")
    root_node.print()
    traverse_tree(root_node)
    search_for_variables_in_tree(root_node)
    search_for_variable_without_tree(nodes_list)
    print("\n---------")
    print("VARIABLES")
    print("---------")
    for key, value in variable_nodes.items():
        print("TYPE: " + key)
        print("PATH:")
        value.variable_print()
        print(key)
        print(value.text)
