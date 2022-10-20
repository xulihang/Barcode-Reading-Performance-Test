import cv2

class ObjectDetector():
    def __init__(self):
        self.model = cv2.dnn_DetectionModel("qrcode.weights","qrcode.cfg")
        self.model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

    def decode_file(self, img_path,return_img=False):
        result_dict = {}
        results = []
        img = cv2.imread(img_path)
        
        classes, scores, boxes = self.model.detect(img,0.2,0.5)
        count = len(boxes)
        for i in range(count):
            result = {}
            result["barcodeFormat"] = ""
            result["barcodeText"] = ""
            x = boxes[i][0]
            y = boxes[i][1]
            width = boxes[i][2]
            height = boxes[i][3]
            result["x1"] = int(x)
            result["y1"] = int(y)
            result["x2"] = int(x + width)
            result["y2"] = int(y)
            result["x3"] = int(x + width)
            result["y3"] = int(y + height)
            result["x4"] = int(x)
            result["y4"] = int(y + height)
            bbox = {}
            bbox["left"] = int(x)
            bbox["top"] = int(y)
            bbox["width"] = int(width)
            bbox["height"] = int(height)
            result["bbox"] = bbox
            result["confidence"] = float(scores[i])
            results.append(result)
        result_dict["results"] = results
        if return_img:
            return result_dict, img
        else:
            return result_dict
        
if __name__ == '__main__':
    import time
    reader = ObjectDetector()
    start_time = time.time()
    results = reader.decode_file("17-damaged-barcodes.png")
    end_time = time.time()
    elapsedTime = int((end_time - start_time) * 1000)
    print(results)
    print(elapsedTime)
    