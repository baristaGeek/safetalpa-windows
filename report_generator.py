#First attemp at the backend
import os
#Creating a new folder for taking the data
current_directory = os.getcwd()
folder_name = 'Malware detected'
final_directory = os.path.join(current_directory, folder_name)
if not os.path.exists(final_directory):
    os.makedirs(final_directory)

def defineDataToSend(kind, data):
    if kind == 0:
        addProcceses(data)
    elif kind == 1:
        addLoggedUsers(data)
    elif kind == 2:
        addConectionPorts(data)
def addProcceses(proccesToAdd):
    process_running_file = open(final_directory + "\\malwareProces.csv","a+")
    process_running_file.write(proccesToAdd)
    process_running_file.close()
def addLoggedUsers(loggedUsersToAdd):
    users_file = open(final_directory + "\\malwareUsers.csv","a+")
    users_file.write(loggedUsersToAdd)
    users_file.close()
def addConectionPorts(conectionsToAdd):
    conection_files = open(final_directory + "\\malwareConections.csv","a+")
    conection_files.write(conectionsToAdd)
    conection_files.close()   
