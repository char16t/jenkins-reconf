## Problem

Change part of configuration in a lot of jobs. For example update the plugin.
Configuration of CI jobs is almost same but not identical.

## Solution

This script support:

 1. Step-by-step execution or automated execution
 2. Backups of CI-job configurations
 3. Custom actions (works with part of XML configuration, modify it as you want)

Just add CI-jobs urls to `modify.txt` and run script.

Output example:

```
[09-10-2019 12:43:58] Starting migration process...
[09-10-2019 12:44:23] STEP 1: Getting all CI jobs
[09-10-2019 12:46:35] STEP 2: Backing up configuration of CI jobs
[09-10-2019 12:47:12] STEP 3: Reconfigure locally saved CI jobs configs
[09-10-2019 12:48:01] STEP 4: Disable all CI jobs before re-configuration
[09-10-2019 12:49:03] STEP 5: Apply new configuration to CI jobs
[09-10-2019 12:50:13] STEP 6: Enable all CI jobs after re-configuration
```

## Usage

 0. Install [python-requests](http://docs.python-requests.org/en/master/) library
 1. Open and edit `config.py` file
 2. Execute `python reconf.py` (Python 2)
 
## Configuration

### Manual control mode

In manual mode, user confirmation is requested before each next step. To 
continue, enter "Y", " y " or press Enter.

If manual mode is disabled, the script will execute step by step.
 
Enable manual control mode

```
     MANUAL_MODE = True
```

Disable manual control mode

```
     MANUAL_MODE = False
```

### URL with list of CI-jobs

From this address will be collected all jobs in which you want to make changes.

```
CI_URL_PREFIX = "https://cisrv.yourcompany.com/view/myview/"
```

### Disable collecting CI-jobs from Jenkins

Set `USE_JOB_LIST = True` to disable collecting CI-jobs from CI_URL_PREFIX 
(previous parameter). List of CI-jobs will be taken from file.

```
USE_JOB_LIST = True
JOB_LIST_FILE = "modify.txt"
```

### User

Domain user. Inside yourcompany'а any requests to Jenkins CI servers can be 
available from some domain user.

```
USERNAME = "valeriy"
```

### Password

Password of domain user.

```
PASSWORD = "your_password"
```

### Name of directory with data

When you run script, a directory will be created in the same place where it
is script. It will record logs, configuration CI job and in General any files 
and data related to the last run of script. You can set any static name:

```
     LOCAL_STORAGE_DIR = "process"
```

or generate it automatically for every execution: For example, you can create
directory that contains timestamp in name:

```     
     LOCAL_STORAGE_DIR = "process-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
```

### Logging

This script logs actions and errors in sufficient detail. All this information
is recorded in a file. The file is always supplemented and never deleted,
not renamed, not replaced by a new one. 

```
LOG_FILE_NAME = "log.txt"
```

### Name of directory with original CI-jobs configuration

Before editing configuration on Jenkins servers, script saves 
original configuration of modified CI jobs so that it can be later 
recover if something goes wrong. Original configuration is stored in
XML files in the directory: `LOCAL_STORAGE_DIR/CI_JOBS_CONFIGS_DIR`

```
CI_JOBS_CONFIGS_DIR = "jobs"
```

### Name of directory with changed CI-jobs configuration

Before editing configuration on Jenkins servers, script makes 
changes in initial configuration of a CI job locally. Modified 
configuration is stored as XML files in the directory: `LOCAL_STORAGE_DIR/CI_JOBS_RECONFIGS_DIR`

```
CI_JOBS_RECONFIGS_DIR = "new_jobs"
```

### Action

Function that performs a configuration conversion. Receives the file. Returns 
modified XML configuration as a string.

```
def action(job_config):
    pass
```

## Unlicense

This is a public domain. Do whatever you want with this code.
