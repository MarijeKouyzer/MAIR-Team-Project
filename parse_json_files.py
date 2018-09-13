import os
from re import match
import json

dialogues = []


def main():
    iterate_over_folders(read_json_files)
    write_dialogue_list_to_file()


def write_to_dialogue_list(dialogue: str):
    dialogues.append(dialogue)


def write_dialogue_list_to_file():
    dialogues_as_text = json.dumps(dialogues)
    with open("dialogues.json", "rw") as f:
        f.write(dialogues_as_text)
        f.close()


def read_json_files(write_function: function, dialogue_id: str):
    pass


def directory_name_is_identifier(name):
    return match(r"voip-.*", name) is not None


def iterate_over_folders(node_function: function, parent_dir = ""):
    for name in os.listdir("."):
        if directory_name_is_identifier(parent_dir):
            node_function(write_to_dialogue_list, parent_dir)
        elif os.path.isdir(name):
            iterate_over_folders(read_json_files, name)


main()
print("Dialogues file created")
