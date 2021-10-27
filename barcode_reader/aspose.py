from asposebarcode import Assist
from asposebarcode.Recognition import *

class AsposeBarcodeReader():
    def __init__(self):
        license = Assist.License()
        license.setLicense("Aspose.BarCode.Python.Java.lic")
        self.reader = BarCodeReader(None,None,None)
        
    def decode_file(self, img_path):
        result_dict = {}
        results = []
        self.reader.setBarCodeReadType([ DecodeType.UPCA, DecodeType.EAN_13 ])
        self.reader.setBarCodeImage(img_path,None)
        for barcode in self.reader.readBarCodes():
            print(barcode)
            result = {}
            result["barcodeFormat"] = barcode.getCodeTypeName()
            result["barcodeText"] = barcode.getCodeText()
            result["confidence"] = barcode.getConfidence().value
            points = barcode.getRegion().points
            result["x1"] =points[0].getX()
            result["y1"] =points[0].getY()
            result["x2"] =points[1].getX()
            result["y2"] =points[1].getY()
            result["x3"] =points[2].getX()
            result["y3"] =points[2].getY()
            result["x4"] =points[3].getX()
            result["y4"] =points[3].getY()
            results.append(result)
        result_dict["results"] = results
        
        return result_dict

if __name__ == '__main__':
    import time
    reader = AsposeBarcodeReader()
    start_time = time.time()
    results = reader.decode_file("F:\\test\\qr_code.png")
    end_time = time.time()
    elapsedTime = int((end_time - start_time) * 1000)
    print(results)
    print(elapsedTime)
    
    start_time = time.time()
    results = reader.decode_file("F:\\[P]ISBN_18_0002.jpg")
    end_time = time.time()
    elapsedTime = int((end_time - start_time) * 1000)
    print(results)
    print(elapsedTime)
    