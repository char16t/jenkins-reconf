from time import sleep
import datetime
import sys
import os
import urllib2
import json
import base64
import xml.etree.ElementTree as ET
import requests
from shutil import copyfile

from config import MANUAL_MODE, USERNAME, PASSWORD, LOG_FILE_NAME, LOCAL_STORAGE_DIR, CI_JOBS_CONFIGS_DIR, CI_JOBS_RECONFIGS_DIR, CI_URL_PREFIX, action, USE_JOB_LIST, JOB_LIST_FILE

CI_URL_JOB_PREFIX = CI_URL_PREFIX + "job/"
CI_URL_API_PREFIX = CI_URL_PREFIX + "api/json"

def log(message):
    """
    Write log message to stdout and  to predefined file
    """
    time = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] "
    outmsg = time + message
    print(outmsg)
    with open(LOCAL_STORAGE_DIR + "/" + LOG_FILE_NAME, "a") as myfile:
        myfile.write(outmsg + "\n")

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def ask_continue(question):
    """
    Ask YES or NO and break program if user answered NO
    """
    if not MANUAL_MODE:
        return
    answer = query_yes_no(question)
    if answer == 'no':
        print("Migration process has been stopped manually")
        exit(1)

def make_request(url):
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (USERNAME, PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    result = urllib2.urlopen(request)
    data = json.load(result)
    return data
    
def make_request_raw(url):
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (USERNAME, PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    content = ""
    try:
        result = urllib2.urlopen(request)
        content = result.read()
    except Exception as details:
        log("Request to " + url + " failed Exception: \n" + str(details))
    return content
        
def prepare_local_storage():
    if not os.path.exists(LOCAL_STORAGE_DIR):
        os.makedirs(LOCAL_STORAGE_DIR)
    if not os.path.exists(LOCAL_STORAGE_DIR + "/" + CI_JOBS_CONFIGS_DIR):
        os.makedirs(LOCAL_STORAGE_DIR + "/" + CI_JOBS_CONFIGS_DIR)
    if not os.path.exists(LOCAL_STORAGE_DIR + "/" + CI_JOBS_RECONFIGS_DIR):
        os.makedirs(LOCAL_STORAGE_DIR + "/" + CI_JOBS_RECONFIGS_DIR)

def get_list_of_ci_jobs():
    if USE_JOB_LIST:
        copyfile(JOB_LIST_FILE, LOCAL_STORAGE_DIR + "/jobs.txt")
        return
    url = CI_URL_API_PREFIX
    data = make_request(url)
    jobs = data['jobs']
    with open(LOCAL_STORAGE_DIR + "/" + "jobs.txt", "a") as jobs_file:
        for job in jobs:
            if job['name'].startswith('RES_') and job['name'].endswith('_RESERVE_SDP'):
                log("Job " + job['name'] + " has been skipped (reserved job)")
                continue
            log("Getting configuration of " + job['name'] + " job")
            jobs_file.write(job['name'] + "\n")

def get_ci_jobs_configuration():
    jobs = [line.rstrip('\n') for line in open(LOCAL_STORAGE_DIR + "/" + "jobs.txt")]
    for job in jobs:
        log("Getting configuration of " + job + " job")
        content = make_request_raw(CI_URL_JOB_PREFIX + job + "/config.xml")
        with open(LOCAL_STORAGE_DIR + "/" + CI_JOBS_CONFIGS_DIR + "/" + job + ".xml", "w") as job_config:
            job_config.write(content)

def reconfigure_ci_jobs():
    jobs = [line.rstrip('\n') for line in open(LOCAL_STORAGE_DIR + "/" + "jobs.txt")]
    for job in jobs:
        log("Reconfigure " + job + " job")
        with open(LOCAL_STORAGE_DIR + "/" + CI_JOBS_CONFIGS_DIR + "/" + job + ".xml", "r") as job_config:
            with open(LOCAL_STORAGE_DIR + "/" + CI_JOBS_RECONFIGS_DIR + "/" + job + ".xml", "w") as job_reconfig:
                try:
                    modified = action(job_config)
                    job_reconfig.write(modified)
                except Exception as e:
                    log("Job " + job + " has not been reconfigured. Exception:\n" + str(e))

def disable_ci_jobs():
    jobs = [line.rstrip('\n') for line in open(LOCAL_STORAGE_DIR + "/" + "jobs.txt")]
    for job in jobs:
        log("Disable " + job + " job")
        url = CI_URL_JOB_PREFIX + job + "/disable"
        r = requests.post(url, auth=(USERNAME, PASSWORD))
        if r.status_code != 200:
            log("Warning: Disabling job " + job + "... (status " + str(r.status_code) + ")")

def apply_ci_jobs_configuration():
    jobs = [line.rstrip('\n') for line in open(LOCAL_STORAGE_DIR + "/" + "jobs.txt")]
    for job in jobs:
        log("Apply configuration to " + job + " job")
        url = CI_URL_JOB_PREFIX + job + "/config.xml"
        headers = {"Content-Type" : "application/xml"}
        with open(LOCAL_STORAGE_DIR + "/" + CI_JOBS_RECONFIGS_DIR + "/" + job + ".xml", "r") as job_config:
            xml_config = job_config.read()
            r = requests.post(url, auth=(USERNAME, PASSWORD), data=xml_config, headers=headers)
            if r.status_code != 200:
                log("Warning: Applying configuration to job " + job + "... (status " + str(r.status_code) + ")")
            sleep(1)

def enable_ci_jobs():
    jobs = [line.rstrip('\n') for line in open(LOCAL_STORAGE_DIR + "/" + "jobs.txt")]
    for job in jobs:
        log("Enable " + job + " job")
        url = CI_URL_JOB_PREFIX + job + "/enable"
        r = requests.post(url, auth=(USERNAME, PASSWORD))
        if r.status_code != 200:
            log("Warning: Enabling job " + job + "... (status " + str(r.status_code) + ")")                

def restore_jobs_from_backup():
    jobs = [line.rstrip('\n') for line in open(LOCAL_STORAGE_DIR + "/" + "jobs.txt")]
    for job in jobs:
        log("Restore job " + job + " from backup")
        url = CI_URL_JOB_PREFIX + job + "/config.xml"
        headers = {"Content-Type" : "application/xml"}
        with open(LOCAL_STORAGE_DIR + "/" + CI_JOBS_CONFIGS_DIR + "/" + job + ".xml", "r") as job_config:
            xml_config = job_config.read()
            r = requests.post(url, auth=(USERNAME, PASSWORD), data=xml_config, headers=headers)
            if r.status_code != 200:
                log("Warning: Restoring job " + job + "from backup... (status " + str(r.status_code) + ")")
            
def main():
    """
    Entry point
    """
    
    ask_continue("Are you ready to prepare local storage?")
    prepare_local_storage()
    
    log("Starting migration process...")
    
    ask_continue("Are you ready to getting all CI jobs?")
    log("STEP 1: Getting all CI jobs")
    get_list_of_ci_jobs()
    
    ask_continue("Are you ready to backing up configuration of CI jobs?")
    log("STEP 2: Backing up configuration of CI jobs")
    get_ci_jobs_configuration()
    
    ask_continue("Are you ready to reconfigure locally saved CI jobs configs?")
    log("STEP 3: Reconfigure locally saved CI jobs configs")
    reconfigure_ci_jobs()
    
    ask_continue("Are you ready to disable all CI jobs before re-configuration?")
    log("STEP 4: Disable all CI jobs before re-configuration")
    disable_ci_jobs()

    ask_continue("Are you ready to apply new configuration to CI jobs?")
    log("STEP 5: Apply new configuration to CI jobs")
    apply_ci_jobs_configuration()
    
    ask_continue("Are you ready to enable all CI jobs after re-configuration?")
    log("STEP 6: Enable all CI jobs after re-configuration")
    enable_ci_jobs()
    
    log("STEP 7: Back up")
    restore_jobs_from_backup()
    
    log("Finishing reconfiguration process...")
  
if __name__ == '__main__':
    main()
