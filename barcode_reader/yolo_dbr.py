import cv2
import sys
sys.path.append("..")
from barcode_reader.object_detection import ObjectDetector
from barcode_reader.dynamsoft import DynamsoftBarcodeReader

class YOLODBR():
    def __init__(self,crop=True):
        self.yolo = ObjectDetector()
        self.dbr = DynamsoftBarcodeReader()
        self.crop = crop

    def decode_file(self, img_path):
        yolo_result_dict, img = self.yolo.decode_file(img_path,return_img=True)
        yolo_results = yolo_result_dict["results"]
        if self.crop:
            self.update_expected_code_count(1)
            result_dict = {}
            results = []
            result_dict["results"] = results
            for result in yolo_results:
                bbox = result["bbox"]
                x = bbox["left"]
                y = bbox["top"]
                w = bbox["width"]
                h = bbox["height"]
                crop = img[y:y+h, x:x+w]
                results_of_crop = self.dbr.decode_buffer(crop)["results"]
                self.restore_localization_points(results_of_crop, x, y)
                results.extend(results_of_crop)
        else:
            expected_count = len(yolo_results)
            print(expected_count)
            self.update_expected_code_count(expected_count)
            result_dict = self.dbr.decode_buffer(img)
        
        print(len(result_dict["results"]))
        
        return result_dict
        
    def update_expected_code_count(self, expected_count):
        settings = self.dbr.dbr.get_runtime_settings()
        settings.expected_barcodes_count = expected_count
        try:
            self.dbr.dbr.update_runtime_settings(settings)
        except BarcodeReaderError as e:
            print(e)
        
    def restore_localization_points(self,results, x, y):
        for result in results:
            result["x1"] = result["x1"] + x
            result["y1"] = result["y1"] + y
            result["x2"] = result["x2"] + x
            result["y2"] = result["y2"] + y
            result["x3"] = result["x3"] + x
            result["y3"] = result["y3"] + y
            result["x4"] = result["x4"] + x
            result["y4"] = result["y4"] + y
            
        
if __name__ == '__main__':
    import time
    reader = YOLODBR()
    start_time = time.time()
    results = reader.decode_file("17-damaged-barcodes.png")
    end_time = time.time()
    elapsedTime = int((end_time - start_time) * 1000)
    print(results)
    print(elapsedTime)
    