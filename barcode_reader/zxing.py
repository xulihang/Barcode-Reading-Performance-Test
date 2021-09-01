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
                if "parsed" in tr:
                    result = {}
                    result["barcodeFormat"] = tr["format"].decode("utf-8")
                    result["barcodeText"] = tr["parsed"].decode("utf-8")
                    points = tr["points"]
                    left=points[0][0]
                    top=points[0][1]
                    right=points[1][0]
                    bottom=points[1][1]
                    for point in points:
                        left = min(left,point[0])
                        top = min(top,point[1])
                        right = max(right,point[0])
                        bottom = max(bottom,point[1])
                    result["x1"] = left
                    result["y1"] = top
                    result["x2"] = right
                    result["y2"] = top
                    result["x3"] = right
                    result["y3"] = bottom
                    result["x4"] = left
                    result["y4"] = bottom
                    results.append(result)
        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = ZXingBarcodeReader()
    results = reader.decode_file("black_qr_code.png")
    print(results)