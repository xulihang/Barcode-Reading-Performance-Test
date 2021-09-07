import os

def rename_files_in_dir(folder, find, replace):
    for filename in os.listdir(folder):
        path = os.path.join(folder,filename)
        if os.path.isdir(path):
            rename_files_in_dir(path,find,replace)
        else:
            if filename.find(find)!=-1:
                os.rename(path,path.replace(find,replace))
                
                

rename_files_in_dir("D:\\test\\BarcodePerformance\\new\\tmp\\","-commandline.json","-scandit.json")