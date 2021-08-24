import EAN13_Reader.detect as detector
import EAN13_Reader.decode as decoder
import cv2
import os
import numpy as np


class EAN13Reader():
    def __init__(self):
        pass

    def decode_file(self, img_path):
        result_dict = {}
        results = []        
        image = cv2.imread(img_path)
        candidates = detector.detect(image)
        for i in range(len(candidates)):
            candidate = candidates[i]
            cropped = candidate["cropped"]
            rect = candidate["rect"]
            box = cv2.boxPoints(rect) 
            box = np.int0(box)
            ean13, is_valid, thresh = decoder.decode(cropped)
            if is_valid:
                result = {}
                result["barcodeFormat"] = "EAN13"
                result["barcodeText"] = ean13
                result["x1"] = int(box[0][0])
                result["y1"] = int(box[0][1])
                result["x2"] = int(box[1][0])
                result["y2"] = int(box[1][1])
                result["x3"] = int(box[2][0])
                result["y3"] = int(box[2][1])
                result["x4"] = int(box[3][0])
                result["y4"] = int(box[3][1])
                results.append(result)

        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = EAN13Reader()
    results = reader.decode_file("test.jpg")
    print(results)
    