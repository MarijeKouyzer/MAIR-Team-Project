import json
import os


def write_dialog_file(session_id,task,dialog):
    dia_file = open("dia_file.txt", "ab")
    dia_file.write(bytes(session_id + "\n", 'utf-8'))
    dia_file.write(bytes(task + "\n", 'utf-8'))
    for str in dialog:
        dia_file.write(bytes(str + "\n", 'utf-8'))

def make_dialog(label_path,log_path):
    # Trying to create a dialogue from both jason files
    json_file = open(label_path, "r", encoding="utf-8")
    label = json.load(json_file)
    json_file.close()

    json_file = open(log_path, "r", encoding="utf-8")
    log = json.load(json_file)
    json_file.close()

    turn = 0
    customer = []
    system = []

    dialog = []
    session_id = log["session-id"]
    task = label["task-information"]["goal"]["text"]

    for i in log["turns"]:
        # print(i["output"]["transcript"])
        system.append(i["output"]["transcript"])
        turn += 1

    for i in label["turns"]:
        # print(i["transcription"])
        customer.append(i["transcription"])

    # Combine log and label
    for i in range(0, turn):
        dialog.append(system[i])
        dialog.append(customer[i])
    write_dialog_file(session_id,task,dialog)

def path_traverse():
    for curDir, dirs, files in os.walk("dstc2_traindev.tar"):
        """""       
        print('=======For Folder Tracing============')
        print("現在のディレクトリ: " + curDir)
        print("内包するディレクトリ:" + ' '.join(dirs))
        print("内包するファイル: " + ' '.join(files))
        """""
        file_to_open1 = os.path.join(curDir,"label.json")
        file_to_open2 = os.path.join(curDir, "log.json")

        if os.path.isfile(file_to_open1) and os.path.isfile(file_to_open2):
            make_dialog(file_to_open1,file_to_open2)
        """""
        #For Folder Tracing
        else:
            print("Files not exist!")
        """""
def main():
    path_traverse()

main()





