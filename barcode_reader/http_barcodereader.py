import json
import requests
import os
import base64


class HTTPBarcodeReader():
    def __init__(self, sdk="MLKit",url="http://192.168.31.103:8888/"):
        self.url = url
        self.sdk = sdk
        if os.path.exists("qrcode.png"):
            self.decode_file("qrcode.png")
    
    def decode_file(self, img_path):
        with open(img_path, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
        print(b64_string)
        r = requests.post('http://192.168.31.103:8888/', json = {'base64':b64_string.decode("utf-8"),'sdk':self.sdk})
        result_dict = r.text
        return result_dict
        
if __name__ == '__main__':

    reader = HTTPBarcodeReader()
    
    results = reader.decode_file("F:\\[P]ISBN_18_0002.jpg")
    print(results)
    