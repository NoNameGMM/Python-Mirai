import subprocess
from lightningrobot.adapter import Adapter
from lightningrobot import log
import os
import sys


current_directory = os.path.dirname(os.path.realpath(__file__))
command = 'python' + " " + current_directory + "/client.py"
process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

while True:
        try:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print(output.decode('gbk', errors='replace'), end='')
        except KeyboardInterrupt:
            log.info("正在退出Mirai适配...")
            process.kill()
            sys.exit()