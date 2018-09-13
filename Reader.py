import json
import os

# First trying to create a dialogue from jason

current_folder = os.getcwd()
data_folder = os.path.join(current_folder,"dstc2_traindev.tar/data/Mar13_S0A0/voip-00d76b791d-20130327_010416")

file_to_open = os.path.join(data_folder, "label.json")
json_file = open(file_to_open,"r",encoding="utf-8")
label = json.load(json_file)
json_file.close()

file_to_open = os.path.join(data_folder, "log.json")
json_file = open(file_to_open,"r",encoding="utf-8")
log = json.load(json_file)
json_file.close()

turn = 0
customer = []
system = []
dialog = []
session_id = log["session-id"]
task = label["task-information"]["goal"]["text"]


for i in log["turns"]:
    #print(i["output"]["transcript"])
    system.append(i["output"]["transcript"])
    turn += 1

for i in label["turns"]:
    #print(i["transcription"])
    customer.append(i["transcription"])

#Combine log and label
for i in range(0,turn):
    dialog.append(system[i])
    dialog.append(customer[i])
print(dialog)

#Write to File
dia_file = open("dia_file.txt","wb")
dia_file.write(bytes(session_id + "\n" ,'utf-8'))
dia_file.write(bytes(task + "\n" ,'utf-8'))
for str in dialog :
    dia_file.write(bytes(str + "\n" ,'utf-8'))





