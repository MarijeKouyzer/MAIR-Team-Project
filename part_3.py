from sentence_to_node_converter import SentenceToNodeConverter
from sentence_tree_builder import SentenceTreeBuilder
from variable_extractor import VariableExtractor

while True:
    user_text = input("Enter text to evaluate: ")
    nodes_list = SentenceToNodeConverter().build_node_list(user_text)
    root_node = SentenceTreeBuilder().build_tree(nodes_list)
    variable_nodes = dict()
    print("The root node will be ", root_node.text)
    print("TREE")
    print("--------")
    root_node.print()
    variable_extractor = VariableExtractor()
    variable_extractor.traverse_tree(root_node)
    variable_extractor.search_for_variables_in_tree(root_node)
    variable_extractor.search_for_variable_without_tree(nodes_list)
    print("\n---------")
    print("VARIABLES")
    print("---------")
    for key, value in variable_extractor.variable_nodes.items():
        print("TYPE: " + key)
        print("PATH:")
        value.variable_print()
        print(key)
        print(value.text)
