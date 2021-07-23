#coding=utf-8

import os
from shutil import copyfile

dir1 = {}
dir2 = {}
files = set()

for filename in os.listdir("failed"):
    dir1[filename] = ""
    files.add(filename)
    
for filename in os.listdir("failed-commandline"):
    dir2[filename] = "" 
    files.add(filename)
    
    
for filename in files:
    if (filename in dir1) and (filename in dir2):
        print(filename)
        if os.path.exists("shared") == False:
            os.mkdir("shared")
        img_path = os.path.join("failed",filename)
        
        copyfile(img_path, os.path.join("shared",filename))
        

