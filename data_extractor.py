import os
import json
from re import match


class DataExtractor:

    cwd: str = ""
    out_cwd: str = ""
    dialogues = []
    utterances = dict()
    handled_sessions = []

    def __init__(self, cwd: str, out_cwd: str):
        self.cwd = cwd
        self.out_cwd = out_cwd
        self.iterate_over_folders(path=cwd)
        self.write_dialogue_list_to_file(self.dialogues, self.out_cwd)
        self.write_utterances_to_file(self.utterances, self.out_cwd)

    @staticmethod
    def write_utterances_to_file(utterances: dict, out_cwd: str):
        # Turn dict to string
        file_string = ""
        for key, value in utterances.items():
            file_string += value + " " + key + "\n"
        # Write to file
        with open(os.path.join(out_cwd, "utterances"), "w") as f:
            f.write(file_string)
            f.close()
        #print("Utterances file created!")

    @staticmethod
    def write_dialogue_list_to_file(dialogues, out_cwd):
        dialogues_as_text = json.dumps(dialogues)
        with open(os.path.join(out_cwd, "dialogues.json"), "w") as f:
            f.write(dialogues_as_text)
            f.close()
        #print("Dialogues file created!")

    def iterate_over_folders(self, parent_dir="", path=""):
        # Go over all files in the folder
        for name in os.listdir(path):
            # Make sure that a dialogue is only created once per session id
            if self.directory_name_is_identifier(parent_dir) and parent_dir not in self.handled_sessions:
                self.handled_sessions.append(parent_dir)
                self.read_json_files(path)
            # If the parent_dir was not a dialogue id and the item is a directory
            elif os.path.isdir(os.path.join(path, name)):
                # Update the path
                new_path = os.path.join(path, name)
                self.iterate_over_folders(name, new_path)

    def read_json_files(self, path: str):
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
        dialogue = "session id: " + log["session-id"] + "\n"
        dialogue += label["task-information"]["goal"]["text"] + "\n"

        # Go through each turn and show the system and the user turns
        for i, system_turn in enumerate(log["turns"]):
            user_turn = label["turns"][i]
            readable_system = "system: " + system_turn["output"]["transcript"] + "\n"
            readable_user = "user: " + user_turn["transcription"] + "\n"
            dialogue += readable_system + readable_user

            # Write an utterance-speech_act combination to the part2 data
            cam = user_turn["semantics"]["cam"]
            utterance = user_turn["transcription"]
            speech_act = cam.split('(')[0]
            self.utterances[utterance] = speech_act

        # Write the dialogue to the list
        self.dialogues.append(dialogue)

    @staticmethod
    def directory_name_is_identifier(name):
        return match(r"voip-.*", name) is not None
