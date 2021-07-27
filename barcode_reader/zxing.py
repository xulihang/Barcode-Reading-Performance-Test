from pyzxing import BarCodeReader
import os


class ZXingBarcodeReader():
    def __init__(self):
        self.reader = BarCodeReader()

    def decode_file(self, img_path):
        result_dict = {}
        results = []
        text_results = self.reader.decode(img_path)
        
        if text_results!=None:
            for tr in text_results:
                result = {}
                result["barcodeFormat"] = tr["format"].decode("utf-8")
                result["barcodeText"] = tr["parsed"].decode("utf-8")
                results.append(result)
        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = ZXingBarcodeReader()
    results = reader.decode_file("D:\\test\\BarcodePerformance\\test.jpg")
    print(results)
    