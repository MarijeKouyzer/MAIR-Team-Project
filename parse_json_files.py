import os
import argparse
import sys
from re import match
import json

dialogues = []
handled_sessions = []

parser = argparse.ArgumentParser()
parser.add_argument("--dstc2_dir", "-d",
                    help="Directory of the extracted tar.gz",
                    type=str,
                    default=os.getcwd())
parser.add_argument("--out", "-o",
                    help="Directory for the dialogues json file",
                    type=str,
                    default=os.getcwd())
args = parser.parse_args()
cwd = args.dstc2_dir
out_cwd = args.out
if not os.path.isdir(cwd):
    sys.exit("The dstc2_dir was not a dir. Please check your variables and try again!")
if not os.path.isdir(out_cwd):
    sys.exit("The out path was not a dir. Please check your variables and try again!")


def main():
    iterate_over_folders(read_json_files)
    write_dialogue_list_to_file()


def write_to_dialogue_list(dialogue: str):
    dialogues.append(dialogue)


def write_dialogue_list_to_file():
    dialogues_as_text = json.dumps(dialogues)
    with open(os.path.join(out_cwd, "dialogues.json"), "w") as f:
        f.write(dialogues_as_text)
        f.close()


def read_json_files(write_function, path: str):
    label_path = os.path.join(path, "label.json")
    log_path = os.path.join(path, "log.json")

    if not os.path.isfile(log_path):
        return

    if not os.path.isfile(label_path):
        return

    # Load the json objects from the files
    json_file = open(label_path, "r", encoding="utf-8")
    label = json.load(json_file)
    json_file.close()

    json_file = open(log_path, "r", encoding="utf-8")
    log = json.load(json_file)
    json_file.close()

    # Make an opening for the dialogue
    dialogue = ""
    dialogue += "session id: " + log["session-id"] + "\n"
    dialogue += label["task-information"]["goal"]["text"] + "\n"

    # Go through each turn and show the system and the user turns
    for i, system_turn in enumerate(log["turns"]):
        user_turn = label["turns"][i]
        readable_system = "system: " + system_turn["output"]["transcript"] + "\n"
        readable_user = "user: " + user_turn["transcription"] + "\n"
        dialogue += readable_system + readable_user

    # Write the dialogue to the list
    write_function(dialogue)


def directory_name_is_identifier(name):
    return match(r"voip-.*", name) is not None


def iterate_over_folders(node_function, parent_dir="", path=cwd):
    # Go over all files in the folder
    for name in os.listdir(path):
        # Make sure that a dialogue is only created once per session id
        if directory_name_is_identifier(parent_dir) and parent_dir not in handled_sessions:
            handled_sessions.append(parent_dir)
            node_function(write_to_dialogue_list, path)
        # If the parent_dir was not a dialogue id and the item is a directory
        elif os.path.isdir(os.path.join(path, name)):
            # Update the path
            new_path = os.path.join(path, name)
            iterate_over_folders(read_json_files, name, new_path)


main()
print("Dialogues file created")
