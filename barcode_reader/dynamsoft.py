from dbr import *
import os
import base64


class DynamsoftBarcodeReader():
    def __init__(self,use_intermediate_detection_results=False):
        self.dbr = BarcodeReader()
        self.dbr.init_license("t0071fQAAAGq0DuY2Gzi1F+egy4FjulS8TP8ZQS1H6Myh5TPLJ7/oStYc9r1W8/tsqW2CTaa4ifPCRuU6KT1gBpi1BEwujp5XGxQ=")
        if use_intermediate_detection_results:
            settings = self.dbr.get_runtime_settings()
            settings.intermediate_result_types = EnumIntermediateResultType.IRT_TYPED_BARCODE_ZONE
            self.dbr.update_runtime_settings(settings)
        self.load_root_template_if_exists()

    def load_root_template_if_exists(self):
        if os.path.exists("template.json"):
            print("Found template")
            error = self.dbr.init_runtime_settings_with_file("template.json")
            if error[0] != 0:
                print(error[1])
            else:
                return True
        return False
                
    def set_runtime_settings_with_template(self, template):
        error = self.dbr.init_runtime_settings_with_string(template, conflict_mode=EnumConflictMode.CM_OVERWRITE)
        if error[0] != 0:
            print(error[1])
        
    def reset_runtime_settings(self):
        if self.load_root_template_if_exists() == False:
            print("reset settings")
            self.dbr.reset_runtime_settings()
        
    def decode_file(self, img_path, engine=""):
        result_dict = {}
        results = []
        text_results = self.dbr.decode_file(img_path)
        self.wrap_results(results,text_results)
        self.append_intermediate_results(results)
        result_dict["results"] = results
        
        return result_dict
        
    def decode_file_stream(self, image_bytes):
        result_dict = {}
        results = []
        text_results = self.dbr.decode_file_stream(bytearray(image_bytes))
        self.wrap_results(results,text_results)
        self.append_intermediate_results(results)
        result_dict["results"] = results
        
        return result_dict
    
    def wrap_results(self,results,text_results):
        if text_results==None:
            return
        for tr in text_results:
            result = {}
            result["barcodeFormat"] = tr.barcode_format_string
            result["barcodeFormat_2"] = tr.barcode_format_string_2
            result["barcodeText"] = tr.barcode_text
            result["barcodeBytes"] = str(base64.b64encode(tr.barcode_bytes))[2:-1]
            result["confidence"] = tr.extended_results[0].confidence
            points = tr.localization_result.localization_points
            result["x1"] =points[0][0]
            result["y1"] =points[0][1]
            result["x2"] =points[1][0]
            result["y2"] =points[1][1]
            result["x3"] =points[2][0]
            result["y3"] =points[2][1]
            result["x4"] =points[3][0]
            result["y4"] =points[3][1]
            results.append(result)
    
    def append_intermediate_results(self,results):
        intermediateResults = self.dbr.get_all_intermediate_results()
        if intermediateResults!=None:
            for ir in intermediateResults:
                for lr in ir.results:
                    result = {}
                    result["barcodeFormat"] = ""
                    result["barcodeText"] = ""
                    result["type"] = "intermediateResult"
                    points = lr.localization_points
                    result["x1"] =points[0][0]
                    result["y1"] =points[0][1]
                    result["x2"] =points[1][0]
                    result["y2"] =points[1][1]
                    result["x3"] =points[2][0]
                    result["y3"] =points[2][1]
                    result["x4"] =points[3][0]
                    result["y4"] =points[3][1]
                    results.append(result)
            return results
        
        
if __name__ == '__main__':
    import time
    reader = DynamsoftBarcodeReader()
    start_time = time.time()
    results = reader.decode_file("image045.jpg")
    end_time = time.time()
    elapsedTime = int((end_time - start_time) * 1000)
    print(results)
    print(elapsedTime)
    