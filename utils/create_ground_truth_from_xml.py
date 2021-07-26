import os
import xml.etree.ElementTree as ET
import json

def append_barcode(results, barcode):
    result = {}
    result["attrib"] = barcode.attrib
    Values = get_elements(barcode, "Value")
    for Value in Values:
        result["text"] = Value.text
        result["value_attrib"] = Value.attrib
    results.append(result)
                            
def get_elements(root, name):
    children = []
    for child in root:
        if child.tag == name:
            children.append(child)
    return children

for filename in os.listdir("./Markup"):
    if filename.endswith(".xml") == False:
        continue
    tree = ET.parse(os.path.join("./Markup",filename))
    root = tree.getroot()
    pages = root[0]
    results = []
    for page in pages:
        BarcodesRoot = get_elements(page, "Barcodes")[0]
        Barcodes = get_elements(BarcodesRoot, "Barcode")
        for barcode in Barcodes:
            append_barcode(results, barcode)
    name, ext = os.path.splitext(filename)
    txt_path = os.path.join("./Image",name+".txt")
    f = open (txt_path,"w")
    f.write(json.dumps(results))
    f.close()
     
        

    