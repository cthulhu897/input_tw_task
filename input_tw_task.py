#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
from datetime import datetime
import json, sys, getopt

'''
    This scipts aims to efficiently load time in a task of teamwork
    Args:
        1   this.py
        2   person_id that inputs time
        3   task_id to add time to
        4   hours:minutes to load
'''
# Static and default variables
install = 'https://endpoint.teamwork.com'# TeamWork installation URL
key = '' 		# API Key can be obtained at People > Edit my profile > API & Mobile
person_id = "" 		# default person id
task_id = "" 		# offtopic  default task id
day_time="9:00" 			# 9:00 am starts task input time
time_hours = "8" 			# 8 hours default input time
time_minutes = "0" 			# 8 hours default input time
date = datetime.today().strftime('%Y%m%d') # default is today
billable_flag = "1" 		# by default input time is billable

try:
    import requests
except ImportError:
    print("It looks like you don't have the requests module installed.\n")
    print('This can be installed with:\n')
    print('  $ pip install requests\n')
    print('Also see the requests documentation:')
    print("  http://docs.python-requests.org/en/master/user/install/\n")
    sys.exit(1)

try:
    opts, args = getopt.getopt(sys.argv[1:], 'p:d:T:t:h', ['person=', 'date=', 'task=', 'time=', 'help' ])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-p', '--person'):
        person_id = arg
    elif opt in ('-d', '--date'):
        date = arg
    elif opt in ('-T', '--task'):
        task_id = arg
    elif opt in ('-t', '--time'):
        miner_name = arg
    else:
        usage()
        sys.exit(2)

# Helper methods so we don't have to add the installation & authentication
def _get(u, **p):    return requests.get(    install + u, auth=(key, ''), **p)
def _post(u, **p):   return requests.post(   install + u, auth=(key, ''), **p)
def _delete(u, **p): return requests.delete( install + u, auth=(key, ''), **p)
def _put(u, **p):    return requests.put(    install + u, auth=(key, ''), **p)

# Add time to a task, the whole purpouse of using this script 
# = M_A_I_N =
if __name__ == '__main__':
	r = _post(
		('/tasks/' + task_id + '/time_entries.json'),
		headers={'Content-Type': 'application/json'},
		data=json.dumps(
		    {
		        "time-entry": {
		        "description": "",
		        "person-id": person_id,
		        "date": date,
		        "time": "9:00",
		        "hours": time_hours,
		        "minutes": time_minutes,
		        "isbillable": billable_flag,
		        "tags": ""
		        }
		    }
		    ))
	if (r.status_code >= 200 and r.status_code < 300):
		print('Success!: ', r.status_code)
	else:
		print('WARNING: status code is ', r.status_code)
		print('Verify manually that your operation has been executed')
	print (r.json())
