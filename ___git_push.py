from subprocess import Popen
import os
import time
cwd = os.path.dirname(os.path.realpath(__file__)) 
prefix = ""
#cmd_string = prefix + "git checkout -b dev"
#cmd = Popen(cmd_string, shell=True, cwd=cwd)
cmd_string = prefix + "git add *"
cmd = Popen(cmd_string, shell=True, cwd=cwd)
print("Enter Commit Message:")
commit_message = input()
cmd_string = prefix + 'git commit -m "{}"'.format(commit_message)
cmd = Popen(cmd_string, shell=True, cwd=cwd)
cmd_string = prefix + "git push origin dev"
cmd = Popen(cmd_string, shell=False, cwd=cwd)
#
#	Some login stuff from git
time.sleep(100)