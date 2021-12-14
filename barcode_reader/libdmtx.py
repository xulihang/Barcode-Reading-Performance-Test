from pylibdmtx.pylibdmtx import decode
import cv2

class DMTX():
    def decode_file(self, img_path):
        result_dict = {}
        results = []
        text_results = decode(cv2.imread(img_path))
        print(text_results)
        if "elapsedTime" in text_results:
            result_dict["elapsedTime"] = text_results["elapsedTime"]
        if "results" in text_results:
            text_results = text_results["results"]

        
        for tr in text_results:
            result = {}
            result["barcodeFormat"] = "DataMatrix"
            result["barcodeText"] = tr.data.decode("utf-8")
            left=tr.rect.left
            top=tr.rect.top
            right=left + tr.rect.width
            bottom=top + tr.rect.height
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
    reader = DMTX()
    results = reader.decode_file("DMX1a.jpg")
    print(results)