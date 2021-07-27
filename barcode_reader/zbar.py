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
                results.append(result)
        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = ZbarBarcodeReader()
    results = reader.decode_file("D:\\test\\BarcodePerformance\\test.jpg")
    print(results)
    