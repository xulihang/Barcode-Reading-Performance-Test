#coding=utf-8

import os
import json


def create_based_on_filename():
    for filename in os.listdir("./"):
        if filename.endswith(".jpg") == False:
            continue
        ground_truth_list = []
        result = {}
        result["attrib"] = {"Type": "EAN13"}
        result["text"] = filename.split("-")[0]
        result["value_attrib"] = {}
        ground_truth_list.append(result)
        name, ext = os.path.splitext(filename)
        txt_path = name+".txt"
        f = open(txt_path,"w", encoding="utf-8")
        f.write(json.dumps(ground_truth_list))
        f.close()
    
        
create_based_on_filename()

