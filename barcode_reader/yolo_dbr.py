import cv2
import sys
sys.path.append("..")
from barcode_reader.object_detection import ObjectDetector
from barcode_reader.dynamsoft import DynamsoftBarcodeReader

class YOLODBR():
    def __init__(self):
        self.yolo = ObjectDetector()
        self.dbr = DynamsoftBarcodeReader()

    def decode_file(self, img_path):
        yolo_results = self.yolo.decode_file(img_path)["results"]
        expected_count = len(yolo_results)
        print(expected_count)
        settings = self.dbr.dbr.get_runtime_settings()
        settings.expected_barcodes_count = expected_count
        try:
            self.dbr.dbr.update_runtime_settings(settings)
        except BarcodeReaderError as e:
            print(e)
        
        result_dict = self.dbr.decode_file(img_path)
        print(len(result_dict["results"]))
        
        return result_dict
        
if __name__ == '__main__':
    import time
    reader = YOLODBR()
    start_time = time.time()
    results = reader.decode_file("17-damaged-barcodes.png")
    end_time = time.time()
    elapsedTime = int((end_time - start_time) * 1000)
    print(results)
    print(elapsedTime)
    