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
            result["x1"] = tr.position.top_left.x
            result["y1"] = tr.position.top_left.y
            result["x2"] = tr.position.top_right.x
            result["y2"] = tr.position.top_right.y
            result["x3"] = tr.position.bottom_right.x
            result["y3"] = tr.position.bottom_right.y
            result["x4"] = tr.position.bottom_left.x
            result["y4"] = tr.position.bottom_left.y
            results.append(result)
        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = ZXingBarcodeReader()
    results = reader.decode_file("test.jpg")
    print(results)
    