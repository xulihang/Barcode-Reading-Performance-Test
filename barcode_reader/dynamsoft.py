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
    