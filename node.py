class Node:
    text: str = ""
    type: str = ""
    types: list = []

    children: list = []
    parent = None
    return_type = ""
    # 0 or 1
    return_rule = 1

    @staticmethod
    def remove_brackets(word):
        return_word = word
        print("in remove brackets ", return_word)
        if return_word[0] == "(":
            return_word = return_word[1::]
        if return_word[(len(return_word) - 1)] == ")":
            return_word = return_word[:-1]
        print(return_word, " is returned")
        return return_word

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
                    if left_type == self.remove_brackets(expected_left_type):
                        self.type = left_type
                        right.type = right_type
                        self.return_type = self.remove_brackets(right__type_split[1])
                        self.return_rule = 0
                        return True

                left__type_split = left_type.rsplit("/", 1)
                if len(left__type_split) == 2:
                    expected_right_type = left__type_split[1]
                    print("expected: " + expected_right_type + ", actual: " + right_type)
                    if right_type == self.remove_brackets(expected_right_type):
                        self.type = left_type
                        right.type = right_type
                        self.return_type = self.remove_brackets(left__type_split[0])
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