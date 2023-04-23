import requests
import urllib3
import json
import getpass
from datetime import datetime
import conf_diff

date =datetime.now()
date_time = date.strftime("%m-%d-%Y-")


#IGNORE CERTIFICATE WARNINGS. CHANCES ARE YOU DID NOT CREATE A TRUSTED CERT FOR ALL YOUR FIREWALL DEVICES 😊

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#DEFINE VARIABLES FOR USE IN FUNCTIONS

headers = {'Content-Type': 'application/json', 'User-Agent':'REST API Agent'}
cli_path = "/api/cli/"
payload={"commands":["show run user"]}
backup_payload={"commands": ["show run"]}
host = "192.168.1.23"
#fw_user="admin"
#fw_pwd="Bumpers10"

fw_user = input("Username: ")
try:
    fw_pwd = getpass.getpass(prompt = 'Password: ', stream=None)
except Exception as error:
    print('ERROR',error)


def get_backups():
    hosts_file = open('hosts.txt', 'r+')
    with open('hosts.txt') as hosts_file:
        hosts_array = hosts_file.read().splitlines()
        for host in hosts_array:
            log_file = host + "-" + date_time + ".log"
            openlog = open(log_file, "a")
            url = "https://" + host + cli_path
            print(f"*****Connecting to " + host + "*****\n")
            backupresponse = requests.post(url, auth=(fw_user, fw_pwd), data=json.dumps(backup_payload), headers=headers,
                           verify=False)
            backup_data = json.dumps(backupresponse.text)
            bd = backup_data.replace('\\n', '\n')
            print(f"*****Writing configuration to " + log_file + "*****\n")
            openlog.write(bd)

    openlog.close()
    pass


def compare_conf():
    hosts_file = open('hosts.txt', 'r+')
    with open('hosts.txt') as hosts_file:
        hosts_array = hosts_file.read().splitlines()
        for host in hosts_array:
            change_file = host + "-" + date_time + "-changes.log"
            changelog = open(change_file, "a")
            log_file = host + "-" + date_time + ".log"
            print("*****Comparing Configuration to Template for " + host + "*****\n")
            config_change = conf_diff.ConfDiff(host + "-template.log", log_file)
            cc = config_change.diff()
            cc = cc.replace('[31m', '')
            cc = cc.replace('[39m[32m', '')
            cc = cc.replace('[32m', '')
            cc = cc.replace('[39m', '')
            cc = cc.replace('[33m', '')
            changelog.write(cc)
            print(config_change.diff())

    pass


#MAIN FUNCTION, ONE FUNCTION TO RULE THEM ALL!

if __name__ == "__main__":
    #get_creds()#Get credentials for Login and access to your script to run
    get_backups()# Back it up before you start.
    compare_conf()#compare to template config