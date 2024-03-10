# -*- coding: utf-8 -*-
import requests
import zipfile
from tqdm import tqdm
import os
import sys
import subprocess

current_directory = os.path.dirname(os.path.realpath(__file__))

new_folder_path = current_directory + '/libs'
os.mkdir(new_folder_path)

jython_url = 'https://cdn.nonamegmm.tk/jython/windows/jython.zip'
jdk_url = 'https://mirrors.tuna.tsinghua.edu.cn/Adoptium/17/jdk/x32/windows/OpenJDK17U-jdk_x86-32_windows_hotspot_17.0.10_7.zip'
mirai_url = 'https://maven.aliyun.com/repository/central/net/mamoe/mirai-core-all/2.16.0/mirai-core-all-2.16.0-all.jar'
jython_file = "jython.zip"
jdk_file = "OpenJDK17U-jdk_x86-32_windows_hotspot_17.0.10_7.zip"
mirai_folder = current_directory + "/libs"
mirai_file = mirai_folder + "/mirai-core-all-2.16.0-all.jar"
jython_extract_folder = current_directory + "/jython"
jdk_extract_folder = current_directory


def rename_folder(old_folder_name, new_folder_name):
    try:
        os.rename(old_folder_name, new_folder_name)
        print(f'Folder {old_folder_name} has been renamed to {new_folder_name}')
    except OSError as e:
        print(f'Error: {e}')

old_folder_name = current_directory + "/jdk-17.0.10+7"
new_folder_name = current_directory + '/jdk'


print("---开始下载依赖---")

response = requests.get(jython_url, stream=True)
response1 = requests.get(jdk_url, stream=True)
response2 = requests.get(mirai_url, stream=True)

total_size = int(response.headers.get('content-length', 0))
total_size1 = int(response1.headers.get('content-length', 0))
total_size2 = int(response2.headers.get('content-length', 0))
block_size = 1024 

with open(jython_file, 'wb') as file:
    for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='KB', unit_scale=False):
        file.write(data)
with open(jdk_file, 'wb') as file:
    for data in tqdm(response1.iter_content(block_size), total=total_size1//block_size, unit='KB', unit_scale=False):
        file.write(data)
with open(mirai_file, 'wb') as file:
    for data in tqdm(response2.iter_content(block_size), total=total_size2//block_size, unit='KB', unit_scale=False):
        file.write(data)

with zipfile.ZipFile(jython_file, 'r') as zip_ref:
    zip_ref.extractall(jython_extract_folder)
    response.close()
    
    
with zipfile.ZipFile(jdk_file, 'r') as zip_ref:
    zip_ref.extractall(jdk_extract_folder)
    response1.close()

rename_folder(old_folder_name, new_folder_name)

os.remove(jdk_file)
os.remove(jython_file)
print("---文件解压成功---")
print("---下载文件删除成功---")

os.environ['JAVA_HOME'] = current_directory + '/jdk'

java_bin_dir = os.path.join(os.environ['JAVA_HOME'], 'bin')
os.environ['PATH'] = java_bin_dir + os.pathsep + os.environ.get('PATH', '')

print("已添加环境变量")

command = current_directory + '/jython/bin/jython.exe' + " " + current_directory + "/mirai.py"

process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
while True:
    try:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode('gbk', errors='replace'), end='')
    except KeyboardInterrupt:
        print("正在退出程序...")
        sys.exit()