import subprocess
from lightningrobot.adapter import Adapter
from lightningrobot import log
import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))

os.environ['JAVA_HOME'] = current_directory + '/jdk'

java_bin_dir = os.path.join(os.environ['JAVA_HOME'], 'bin')
os.environ['PATH'] = java_bin_dir + os.pathsep + os.environ.get('PATH', '')
    
command = current_directory + '/jython/bin/jython.exe' + " " + current_directory + "/mirai.py"
process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)