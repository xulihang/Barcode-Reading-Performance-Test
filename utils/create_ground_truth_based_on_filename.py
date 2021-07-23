#coding=utf-8

import os
import json


def create_based_on_filename():
    ground_truth_list = []
    for filename in os.listdir("./"):
        ground_truth = filename.split("-")[0]
        ground_truth_list.append(ground_truth)
    f = open(filename+".txt","w", encoding="utf-8")
    f.write(json.dumps(ground_truth_list))
    f.close()
    
        
create_based_on_filename()

