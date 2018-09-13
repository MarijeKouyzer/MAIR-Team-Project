import json


dialogues = []

with open("dialogues.json", "r") as f:
    dialogues = json.load(f.read()) if f.read() is not "" else []
    f.close()

for dialogue in dialogues:
    print(dialogue)
    input("Press Enter to view the next dialogue...")
