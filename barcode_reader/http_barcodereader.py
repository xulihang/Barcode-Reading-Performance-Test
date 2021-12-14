import json
import requests
import os
import base64


class HTTPBarcodeReader():
    def __init__(self, sdk="MLKit",url="http://192.168.8.68:8888/"):
        self.url = url
        self.sdk = sdk
        self.template = ""
        if os.path.exists("template.json"):
            f = open("template.json", encoding="utf-8")
            self.template = f.read()
            f.close()
        if os.path.exists("qrcode.png"):
            self.decode_file("qrcode.png")
    
    def decode_file(self, img_path):
        with open(img_path, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
        dic = {'base64':b64_string.decode("utf-8"),'sdk':self.sdk}
        if self.template != "":
            dic['template'] = self.template
        r = requests.post(self.url, json = dic)
        result_dict = json.loads(r.text)
        return result_dict
        
if __name__ == '__main__':

    reader = HTTPBarcodeReader()
    
    results = reader.decode_file("F:\\[P]ISBN_18_0002.jpg")
    print(results)
    