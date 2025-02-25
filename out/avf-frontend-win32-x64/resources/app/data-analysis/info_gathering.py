##Capture volatile information of the computer...Windows begining
import subprocess
import datetime
import os
import psutil
import time
from connection_ports import job
#Functions definition
def cleanLoggedOnUsersForCVS(users):
    res = ""
    for line in (str(users)).split("\\n"):
        if line.startswith("b") or line.startswith("'"):
            continue
        line = line.strip()
        line = line.replace("\\r"," ")
        line = line.replace(">","")
        line = " ".join(line.split())
        line = line.replace(" ",",")
        res = res + line + "\n"
    return res
def getProcceses():
    res = ""
    for proc in psutil.process_iter():
        try:
            temp = str(proc.cpu_percent())
            p_name = proc.name()
            p_id = str(proc.pid)
            p_pid = str(proc.ppid())
            p_created_time = str(proc.create_time())
            p_username = proc.username()
            p_status = proc.status()
            p_num_ctx_switches_v = str(proc.num_ctx_switches().voluntary)
            p_num_ctx_switches_i = str(proc.num_ctx_switches().involuntary)
            p_num_handles = str(proc.num_handles())
            p_num_threads = str(proc.num_threads())
            p_cpu_time_user = str(proc.cpu_times().user)
            p_cpu_time_system = str(proc.cpu_times().system)
            p_memory_use_rss = str(proc.memory_info().rss)
            p_memory_use_vms = str(proc.memory_info().vms)
            #theres more in memory use -- https://psutil.readthedocs.io/en/release-3.4.2/#psutil.Process
            p_cpu_percent = str(proc.cpu_percent())
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            pass
        else:
            res = res + p_name + "," + p_id + "," + p_pid + "," + p_created_time + "," + p_username + "," + p_status + "," +p_num_ctx_switches_v + "," + p_num_ctx_switches_i + "," + p_num_handles + "," +  p_num_threads + "," + p_cpu_time_user + "," + p_cpu_time_system + "," + p_memory_use_rss+ "," + p_memory_use_vms + "," + p_cpu_percent + "\n"
    return res
def cleanConections(conections):
    ##chambonada
    listening_in = False 
    syn_sent_in = False
    syn_received_in = False
    established_in = False
    fin_wait_1_in = False
    fin_wait_2_in = False
    close_wait_in = False
    closing_in = False
    last_ack_in = False
    time_wait_in = False
    closed_in = False
    ##chambonada
    res = ""
    for line in (str(conections)).split("\\n"):
        line = line.replace("\\r"," ")
        line = line.strip()
        if line.startswith("b") or line.startswith("Active") or line.startswith("'") or line.startswith("Proto") or not line:
            continue            
        line = line.replace("\\t", ",")
        line = " ".join(line.split())
        if line.startswith("UDP"):
            aux = line.split(" ")
            line = aux[0] + " " +aux[1] +" " + aux[2] +  " none " + aux[3].strip() + "none"
        line = line.replace(" ",",")
        res = res + line + ",1" + "\n"
        aux = line.split(",")
        state = aux[3] 
        if state == "LISTENING":
            listening_in = True
        elif state == "SYN_SENT":
            syn_sent_in = True
        elif state == "SYN_RECEIVED":
            syn_received_in = True
        elif state == "ESTABLISHED":
            established_in = True
        elif state == "FIN_WAIT_1":
            fin_wait_1_in = True
        elif state == "FIN_WAIT_2":
            fin_wait_2_in = True
        elif state == "CLOSE_WAIT":
            close_wait_in = True
        elif state == "CLOSING":
            closing_in = True
        elif state == "LAST_ACK":
            last_ack_in = True
        elif state == "TIME_wAIT":
            time_wait_in = True
        elif closed_in == "CLOSED":
            closed_in = True
    if listening_in == False:
        res = res + "TCP,0.0.0.0:445,0.0.0.0:0,LISTENING,4,InHost" + "\n"
    if syn_sent_in == False:
        res = res + "TCP,1.0.0.0:445,1.0.0.0:0,SYN_SENT,4,InHost" + "\n"
    if syn_received_in == False:
        res = res + "TCP,2.0.0.0:445,2.0.0.0:0,SYN_RECEIVED,4,InHost" + "\n"
    if  established_in == False:
        res = res + "TCP,3.0.0.0:445,3.0.0.0:0,ESTABLISHED,4,InHost" + "\n"
    if fin_wait_1_in == False:
        res = res + "TCP,4.0.0.0:445,4.0.0.0:0,FIN_WAIT_1,4,InHost" + "\n"
    if  fin_wait_2_in == False:
        res = res + "TCP,5.0.0.0:445,5.0.0.0:0,FIN_WAIT_2,4,InHost" + "\n"
    if close_wait_in == False:
        res = res + "TCP,6.0.0.0:445,6.0.0.0:0,CLOSE_WAIT,4,InHost" + "\n"
    if closing_in == False:
        res = res + "TCP,7.0.0.0:445,7.0.0.0:0,CLOSING,4,InHost" + "\n"
    if last_ack_in == False:
        res = res + "TCP,8.0.0.0:445,8.0.0.0:0,LAST_ACK,4,InHost" + "\n"
    if time_wait_in == False:
        res = res + "TCP,9.0.0.0:445,9.0.0.0:0,TIME_WAIT,4,InHost" + "\n"
    if close_wait_in == False:
        res = res + "TCP,0.9.0.0:445,0.9.0.0:0,CLOSE_WAIT,4,InHost" + "\n"
    return res
while True:          
    ##Getting the date and tame of the begginnig of the data gathering
    timestamp_beginning = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    string_timestamp = str(timestamp_beginning)
    #Creating a new folder for taking the data
    current_directory = os.getcwd() +"\\data-analysis\\data_colection"
    folder_name = 'Data for analysis ' + string_timestamp
    final_directory = os.path.join(current_directory, folder_name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    #Getting and saving logged on users
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    logged_on_users = subprocess.Popen("query user",shell = False, stdout=subprocess.PIPE, startupinfo=si).stdout.read()
    logged_on_users_file = open(final_directory + "\\loggedOnUsers.csv","w+")
    logged_on_users_file.write(cleanLoggedOnUsersForCVS(logged_on_users))
    logged_on_users_file.close()
    #Getting the information about the procceses
    process_running_file = open(final_directory + "\\processRunning.csv","w+")
    process_running_file.write(getProcceses())
    process_running_file.close()
    #Getting conections and ports used
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    current_conecctions = subprocess.Popen("netstat -anot",shell = False, stdout=subprocess.PIPE).stdout.read()
    process_running_file = open(final_directory + "\\conectionPorts.csv","w+")
    process_running_file.write(cleanConections(current_conecctions))
    process_running_file.close()
    job()
    time.sleep(120 - time.time() % 120)




