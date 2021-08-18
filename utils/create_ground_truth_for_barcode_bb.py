import os
import json

def get_ground_truth(filename):
    #0022000159342.jpg
    #0022000159342_1.jpg
    if filename.find("_")!=-1:
        return filename[0:filename.find("_")]
    else:
        return filename[0:filename.find(".")]
    

f = open("single_test.txt","r")
for line in f.readlines():
    data = line.strip().split(" ")
    filename = data[0]
    left = data[1]
    top = data[2]
    right = data[3]
    bottom = data[4]
    bbox = {}
    bbox["left"] = left
    bbox["top"] = top
    bbox["right"] = right
    bbox["bottom"] = bottom
    attrib = {}
    attrib["Type"] = "EAN13"
    result = {}
    result["attrib"] = attrib
    result["bbox"] = bbox
    result["text"] = get_ground_truth(filename)
    results = []
    results.append(result)
    fw = open(filename+".txt","w")
    fw.write(json.dumps(results))
    fw.close()
f.close()
