import zxingcpp
from PIL import Image
import os


class ZXingBarcodeReader():
    def __init__(self):
        pass

    def decode_file(self, img_path):
        result_dict = {}
        results = []
        tr = zxingcpp.read_barcode(Image.open(img_path))
        
        if tr.valid == True:
            result = {}
            result["barcodeFormat"] = tr.format.name
            result["barcodeText"] = tr.text
            results.append(result)
        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = ZXingBarcodeReader()
    results = reader.decode_file("2003892380005-01_N95-2592x1944.jpg")
    print(results)
    