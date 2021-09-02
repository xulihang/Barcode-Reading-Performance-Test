import os
import json


def read_data_as_dict(folder_path,filename):
    path=os.path.join(folder_path,filename)
    f=open(path,"r")
    content = f.read()
    f.close()
    
    points_in_lines = False
    if content.find("SET")==-1:
        print(filename)
        print("single code")
        points_in_lines = True
        
    f=open(path,"r")
    lines = f.readlines()
    f.close()
    
    barcodes = []
    barcode = {"attrib": {"Type": "QR"}, "text": "", "value_attrib": {}}
    index = 1
    for line in lines:
        line = line.strip()
        points = line.split(" ")
        print(points)
        print(len(points))
        if len(points)==8:
            barcode = {"attrib": {"Type": "QR"}, "text": "", "value_attrib": {}}
            barcode["x1"] = points[0]
            barcode["y1"] = points[1]
            barcode["x2"] = points[2]
            barcode["y2"] = points[3]
            barcode["x3"] = points[4]
            barcode["y3"] = points[5]
            barcode["x4"] = points[6]
            barcode["y4"] = points[7]
            barcodes.append(barcode)
        if len(points)==2:
            barcode["x"+str(index)] = points[0]
            barcode["y"+str(index)] = points[1]
            index = index+1
    if points_in_lines:
        barcodes.append(barcode)
    return barcodes
    

for category in os.listdir("./"):
    path = os.path.join("./",category)
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".txt"):
                barcodes = read_data_as_dict(path,filename)
                fw=open(os.path.join(path,filename),"w")
                fw.write(json.dumps(barcodes))
                fw.close()
        
