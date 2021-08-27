import cv2

class OpenCV1DReader():
    def __init__(self):
        self.bardet = cv2.barcode_BarcodeDetector()

    def decode_file(self, img_path):
        result_dict = {}
        results = []
        img = cv2.imread(img_path)
        ok, decoded_info, decoded_type, corners = self.bardet.detectAndDecode(img)
        if ok:
            for i in range(len(decoded_info)):
                result = {}
                result["barcodeFormat"] = "EAN13"
                result["barcodeText"] = decoded_info[i]
                points = corners[i]
                result["x1"] = int(points[0][0])
                result["y1"] = int(points[0][1])
                result["x2"] = int(points[1][0])
                result["y2"] = int(points[1][1])
                result["x3"] = int(points[2][0])
                result["y3"] = int(points[2][1])
                result["x4"] = int(points[3][0])
                result["y4"] = int(points[3][1])
                results.append(result)

        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = OpenCV1DReader()
    results = reader.decode_file("multiple.jpg")
    print(results)
    