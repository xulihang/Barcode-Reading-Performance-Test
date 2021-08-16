from dbr import *
import os
import base64


class DynamsoftBarcodeReader():
    def __init__(self):
        self.dbr = BarcodeReader()
        self.dbr.init_license("t0070fQAAAG16DXrR4sc8gNexDekiNrG6xJSiDAabkbAKOyeFtNASIwCzV+Nc6x1GXNVxyJPapcWE++aFwJYBKTFxNqbunQgbAA==")
        if os.path.exists("template.json"):
            print("Found template")
            self.dbr.init_runtime_settings_with_file("template.json")

    def decode_file(self, img_path, engine=""):
        result_dict = {}
        results = []
        text_results = self.dbr.decode_file(img_path)
        
        if text_results!=None:
            for tr in text_results:
                result = {}
                result["barcodeFormat"] = tr.barcode_format_string
                result["barcodeFormat_2"] = tr.barcode_format_string_2
                result["barcodeText"] = tr.barcode_text
                result["barcodeBytes"] = str(base64.b64encode(tr.barcode_bytes))[2:-1]
                result["confidence"] = tr.extended_results[0].confidence
                results.append(result)
                points = tr.localization_result.localization_points
                result["x1"] =points[0][0]
                result["y1"] =points[0][1]
                result["x2"] =points[1][0]
                result["y2"] =points[1][1]
                result["x3"] =points[2][0]
                result["y3"] =points[2][1]
                result["x4"] =points[3][0]
                result["y4"] =points[3][1]
        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    import time
    reader = DynamsoftBarcodeReader()
    start_time = time.time()
    results = reader.decode_file("test.jpg")
    end_time = time.time()
    elapsedTime = int((end_time - start_time) * 1000)
    print(results)
    print(elapsedTime)
    