# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:16:08 2023

@author: py21capb
"""

import os 
import sys

script_templates = "data/script_templates/"


def move_files_bash(molecule1, molecule2):
    find = ["MOLECULE1", "MOLECULE2"]
    replace = [molecule1, molecule2]
    
    if not os.path.exists("data/out/em"):
        os.mkdir("data/out/em")
        
    with open(script_templates + "exp_em_bash.sh", 'r') as f:
        data = f.read()
        for x in range(len(find)):
            data = data.replace(find[x], replace[x])
     
    with open("data/out/em/em_bash.sh", 'w') as f:
        f.write(data)
        
    os.system("dos2unix data/out/em/em_bash.sh")
    os.system("bash data/out/em/em_bash.sh")
    
def move_file_bash(molecule):
    find = ["MOLECULE1"]
    replace = [molecule]
    
    if not os.path.exists("data/out/em"):
        os.mkdir("data/out/em")
    
    with open(script_templates + "exp_single_em_bash.sh", 'r') as f:
        data = f.read()
        for x in range(len(find)):
            data = data.replace(find[x], replace[x])
     
    with open("data/out/em/em_bash.sh", 'w') as f:
        f.write(data)
        
    os.system("dos2unix data/out/em/em_bash.sh")
    os.system("bash data/out/em/em_bash.sh")
        

def create_em_job():
    with open(script_templates + "exp_em_job.sh", 'r') as f:
        data = f.read()
        
    with open("data/out/em/em_job.sh", 'w') as f: 
        f.write(data)
    
if __name__ == "__main__":
    move_files_bash(sys.argv[1], sys.argv[2])
    create_em_job()
