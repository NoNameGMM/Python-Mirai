# -*- coding: utf-8 -*-
import requests
import zipfile
from tqdm import tqdm
import os
import sys
import subprocess
from lightningrobot.adapter import Adapter
from lightningrobot import log

current_directory = os.path.dirname(os.path.realpath(__file__))
block_size = 1024 

new_folder_path = current_directory + '/libs'

old_folder_name = current_directory + "/jdk-17.0.10+7"
new_folder_name = current_directory + '/jdk'

global process, process1

def rename_folder(old_folder_name, new_folder_name):
    os.rename(old_folder_name, new_folder_name)
    
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return process.returncode, output.decode(), error.decode()

class MiraiAdapter(Adapter):
    async def connect(self) -> None:
        log.info("已加载-MiraiAdapter")
        pass
    
    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)

    def install_jython():
        jython_url = 'https://cdn.nonamegmm.tk/jython/windows/jython.zip'
        jython_file = "jython.zip"
        jython_extract_folder = current_directory + "/jython"
        response = requests.get(jython_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        with open(jython_file, 'wb') as file:
            for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='KB', unit_scale=False):
                file.write(data)
        with zipfile.ZipFile(jython_file, 'r') as zip_ref:
            zip_ref.extractall(jython_extract_folder)
            response.close()
        os.remove(jython_file)
        log.info("---文件解压成功---")
        log.info("---下载文件删除成功---")

    def install_jdk():
        jdk_url = 'https://mirrors.tuna.tsinghua.edu.cn/Adoptium/17/jdk/x32/windows/OpenJDK17U-jdk_x86-32_windows_hotspot_17.0.10_7.zip'
        jdk_file = "OpenJDK17U-jdk_x86-32_windows_hotspot_17.0.10_7.zip"
        jdk_extract_folder = current_directory
        response = requests.get(jdk_url, stream=True)
        total_size1 = int(response.headers.get('content-length', 0))
        with open(jdk_file, 'wb') as file:
            for data in tqdm(response.iter_content(block_size), total=total_size1//block_size, unit='KB', unit_scale=False):
                file.write(data)
        with zipfile.ZipFile(jdk_file, 'r') as zip_ref:
            zip_ref.extractall(jdk_extract_folder)
            response.close()
        os.remove(jdk_file)
        rename_folder(old_folder_name, new_folder_name)
        log.info("---文件解压成功---")
        log.info("---下载文件删除成功---")
    
    def install_mirai():
        mirai_url = 'https://repo1.maven.org/maven2/net/mamoe/mirai-core-all/2.16.0/mirai-core-all-2.16.0-all.jar'
        mirai_folder = current_directory + "/libs"
        mirai_file = mirai_folder + "/mirai-core-all-2.16.0-all.jar"
        response = requests.get(mirai_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        with open(mirai_file, 'wb') as file:
            for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='KB', unit_scale=False):
                file.write(data)

    log.info("---开始准备依赖---")
    if os.path.exists(current_directory + "/jython"):
        log.info("依赖项 Jython 已安装")
        if os.path.exists(current_directory + "/jdk"):
            log.info("依赖项 JDK17 已安装")
            if os.path.exists(current_directory + "/libs/mirai-core-all-2.16.0-all.jar"):
                log.info("依赖项 Mirai 已安装")
            else:
                log.info("---安装依赖项:Mirai-Core---")
                install_mirai()
        else:
            log.info("---安装依赖项:JDK17---")
            install_jdk()
    else:
        log.info("---安装依赖项:Jython---")
        install_jython()

    os.environ['JAVA_HOME'] = current_directory + '/jdk'

    java_bin_dir = os.path.join(os.environ['JAVA_HOME'], 'bin')
    os.environ['PATH'] = java_bin_dir + os.pathsep + os.environ.get('PATH', '')

    log.info("已添加JDK环境变量")
    
    command = current_directory + '/jython/bin/jython.exe' + " " + current_directory + "/mirai.py"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    
    command1 = 'python' + " " + current_directory + "/server.py"
    process1 = subprocess.Popen(command1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    
    async def stop(self) -> None:
        log.info("正在退出Mirai适配...")
        process.kill()
        process1.kill()

