import numpy as np
import pyboof as pb



class BoofCVReader():
    def __init__(self):
        pass

    def decode_file(self, img_path):
        result_dict = {}
        results = []
        
        pb.init_memmap()

        # Detects all the QR Codes in the image and prints their message and location

        detector = pb.FactoryFiducial(np.uint8).qrcode()

        image = pb.load_single_band(img_path, np.uint8)

        detector.detect(image)
        
        for qr in detector.detections:
            result = {}
            result["barcodeFormat"] = "QR"
            result["barcodeText"] = qr.message
            result["x1"] = qr.bounds.vertexes[0].x
            result["y1"] = qr.bounds.vertexes[0].y
            result["x2"] = qr.bounds.vertexes[1].x
            result["y2"] = qr.bounds.vertexes[1].y
            result["x3"] = qr.bounds.vertexes[2].x
            result["y3"] = qr.bounds.vertexes[2].y
            result["x4"] = qr.bounds.vertexes[3].x
            result["y4"] = qr.bounds.vertexes[3].y
            results.append(result)

        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = BoofCVReader()
    results = reader.decode_file("test.jpg")
    print(results)
    