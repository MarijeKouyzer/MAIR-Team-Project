import json
import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--dialogue_file", "-d",
                    help="Dialogue file",
                    type=str,
                    default=os.getcwd()+"/dialogues.json")
args = parser.parse_args()
dialogue_file = args.dialogue_file
if not os.path.isfile(dialogue_file):
    sys.exit("The file you entered was not a file. Please try again!")


with open("dialogues.json", "r") as f:
    try:
        dialogues = json.load(f)
    except ValueError:
        dialogues = []
    f.close()

for dialogue in dialogues:
    print(dialogue)
    input("Press Enter to view the next dialogue...")
