import os
import json


def read_data_as_dict(folder_path,filename):
    path=os.path.join(folder_path,filename)
    f=open(path,"r")
    lines = f.readlines()
    f.close()
    barcodes = []
    for line in lines:
        line = line.strip()
        points = line.split(" ")
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
        
