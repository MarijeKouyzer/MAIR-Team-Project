def remove_brackets(word):
    return_word = word
    print("in remove brackets ", return_word)
    # print(return_word[0])
    # print(return_word[(len(word)-1)])
    if return_word[0] == "(":
        # print("must remove ( from ", return_word)
        return_word = return_word[1::]
    if return_word[(len(return_word)-1)] == ")":
        # print("must remove ) from ", return_word)
        # return_word = return_word[::-1] <- I think this is logically incorrect
        return_word = return_word[:-1]
    print(return_word, " is returned")
    return return_word


class Node:
    variable_type: str = ""
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
        print("left ", self.text)
        print("right ", right.text)
        print("*******************")
        for left_type in self.types:
            for right_type in right.types:
                right__type_split = right_type.rsplit("\\", 1)
                if len(right__type_split) == 2:
                    expected_left_type = right__type_split[0]
                    if left_type == expected_left_type:
                        self.type = left_type
                        right.type = right_type
                        self.return_type = remove_brackets(right__type_split[1])
                        self.return_rule = 0
                        return True

                left__type_split = left_type.rsplit("/", 1)
                if len(left__type_split) == 2:
                    expected_right_type = left__type_split[1]
                    if right_type == expected_right_type:
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
    "want": ["(np\s)/np", "(np\s)/np"],
    "a": ["np/np"],
    "restaurant": ["np"],
    "serving": ["(s\s)/np", "(s\s)/np"],
    "swedish": ["np/np", "np/np"],
    "food": ["np"],
    "about": ["np\(s/np)", "pp/np"],
    "an": ["np/np"],
    "and": ["(s\s)/s", "(np\\np)/np"],
    "any": ["np/np"],
    "area": ["np"],
    "can": ["s/(np\s)"],
    "catalan": ["np/np"],
    "center": ["np"],
    "cheap": ["np/np"],
    "chinese": ["np/np"],
    "cuban": ["np/np"],
    "expensive": ["np/np"],
    "find": ["(np\s)/np", "((np\s)/pp)/np"],
    "for": ["pp/np"],
    "have": ["(np\s)/np", "(np\s)/(np\s)"],
    "im": ["s"],
    "in": ["pp/np"],
    "international": ["np/np"],
    "is": ["vp/adjP", "np\((s/pp)/np)"],
    "it": ["np"],
    "serve": ["(np\s)/np"],
    "serves": ["vp/np"],
    "should": ["(np\s)/(np\s)"],
    "like": ["(np\s)/np"],
    "looking": ["s\(s/pp)", "s\((s/pp)/pp)"],
    "moderately": ["adv"],
    "need": ["(np\s)/np", "np"],
    "of": ["np\(np/np)"],
    "part": ["np"],
    "persian": ["np/np"],
    "please": ["s\s"],
    "priced": ["adv\(np/np)", "adv\\adjP"],
    "south": ["np/np"],
    "that": ["(s\s)/vp"],
    "the": ["np/np"],
    "town": ["np"],
    "tuscan": ["np/np"],
    "wanna": ["(np\s)/(np\s)"],
    "west": ["np/np"],
    "what": ["np"],
    "with": ["pp/np"],
    "world": ["np/np"],
    "would": ["np\((s/pp)/np\s))"],
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
    "foods": ["np"],
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
    "needs": ["np", "(np\s)/np"],
    "no": ["np/np"],
    "north": ["np/np"],
    "not": ["np/np", "np"],
    "parts": ["np"],
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
    "restaurants": ["np"],
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
        "keywords": ["town", "of"],
        "words": ["east", "west", "north", "south", "centre"]
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
                  "cubun",
                  "japenese",
                  "catalan"]
    }
}
variable_nodes = dict()


def evaluate_word_list(nodes: list) -> Node:
    tree_node = Node()
    new_nodes = list()
    ori_nodes = nodes

    print(len(ori_nodes))

    global i
    global structure_changed
    i = 0
    structure_changed = False
    while len(ori_nodes) != 1:
        i = 0
        structure_changed = False
        while i <= len(ori_nodes)-1:
            if i < len(ori_nodes)-1:
                if ori_nodes[i].is_compatible_with(ori_nodes[i + 1]):
                    print(i, " is compatible")
                    print(ori_nodes[i].text, " ", ori_nodes[i].return_type)
                    new_node = Node()
                    new_node.children = []
                    new_node.types = [ori_nodes[i].return_type]
                    new_node.type = ori_nodes[i].return_type
                    new_node.text = ori_nodes[i].text + " " + ori_nodes[i+1].text
                    print("new node!", new_node.type, " text: ", new_node.text)
                    new_node.children.append(ori_nodes[i])
                    new_node.children.append(ori_nodes[i+1])
                    ori_nodes[i].parent = new_node
                    ori_nodes[i+1].parent = new_node
                    new_node.print()
                    new_nodes.append(new_node)

                    structure_changed = True
                    if ori_nodes[i].return_rule == 1:
                        print("%%%%%%%%%%% slash 1 rule %%%%%%%%%%%%")
                        i = i+1
                    if ori_nodes[i].return_rule == 0:
                        print("%%%%%%%%%%% slash 0 rule %%%%%%%%%%%%")
                        i = i + 1
                else:
                    print(i, " is not compatible")
                    new_nodes.append(ori_nodes[i])
            else:
                print(i, " is not compatible")
                new_nodes.append(ori_nodes[i])
            i = i + 1

        if structure_changed is True:
            # create new candidates by nodes = new_node_list
            print("structure changed")
            print("#################################")
            print("New nodes")
            for new in new_nodes:
                print(new.text)
            print("new  node length")
            print(len(new_nodes))
            print("#################################")
            ori_nodes = new_nodes
            new_nodes = list()
        if structure_changed is False:
            print("structure not changed")
            break
        # i = i + 1
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Final nodes")
    for new in ori_nodes:
        print(new.text)
    print("Final length")
    print(len(ori_nodes))
    tree_is_complete = len(ori_nodes) == 1
    if tree_is_complete:
        print("Tree is complete")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        tree_node = ori_nodes[0]
        return tree_node
    if structure_changed is False or tree_is_complete is False:
        print("Nothing change or and tree is not complete")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return tree_node
    return Node()


def build_tree(text: str) -> Node:
    # Change the text into a list of nodes containing the word and the type
    word_list = text.split(" ")
    node_list = list()
    # print(word_list)
    for word in word_list:
        word_node = Node()
        word_node.text = word
        if word in rules.keys():
            word_node.types = rules[word]
        else:
            word_node.types = ["np"]
        node_list.append(word_node)
    # Return the tree
    # print(node_list[1].text)
    return evaluate_word_list(node_list)


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


# Wait for input
while True:
    user_text = input("Enter text to evaluate: ").lower()
    root_node = build_tree(user_text)
    variable_nodes = dict()
    print("The root node will be ", root_node.text)
    print("TREE")
    print("--------")
    root_node.print()
    traverse_tree(root_node)
    print("\n---------")
    print("VARIABLES")
    print("---------")
    for key, value in variable_nodes.items():
        print("TYPE: " + key)
        print("PATH:")
        value.variable_print()
