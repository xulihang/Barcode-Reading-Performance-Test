from pyzbar.pyzbar import decode
from PIL import Image
import os


class ZbarBarcodeReader():
    def __init__(self):
        pass

    def decode_file(self, img_path):
        result_dict = {}
        results = []
        text_results = decode(Image.open(img_path))
        
        if text_results!=None:
            for tr in text_results:
                result = {}
                result["barcodeFormat"] = tr.type
                result["barcodeText"] = tr.data.decode("utf-8")
                rect = tr.rect
                result["x1"] = rect.left
                result["y1"] = rect.top
                result["x2"] = rect.left + rect.width
                result["y2"] = rect.top
                result["x3"] = rect.left + rect.width
                result["y3"] = rect.top + rect.height
                result["x4"] = rect.left
                result["y4"] = rect.top + rect.height
                results.append(result)
        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = ZbarBarcodeReader()
    results = reader.decode_file("test.jpg")
    print(results)
    