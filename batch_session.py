#coding=utf-8
import json
import os
import time
import threading
import uuid
import geometry_utils
from shutil import copyfile

class Batch_session():
    def __init__(self, img_folder, output_folder, template=None,session_id=None, name="", recursive=False):
        self.img_folder = img_folder
        self.name = name
        self.output_folder = output_folder
        self.id = uuid.uuid1().hex
        
        if session_id != None:
            self.id = session_id
        self.json_folder = os.path.join(self.output_folder,self.id)
        if os.path.exists(self.json_folder) == False:
            os.mkdir(self.json_folder)
        
        if os.path.exists(os.path.join(self.json_folder,"img_folder")) == False:        
            f = open(os.path.join(self.json_folder,"img_folder"),"w")
            f.write(img_folder)
            f.close()
        
        if os.path.exists(os.path.join(self.json_folder,"name")) == False:
            f = open(os.path.join(self.json_folder,"name"),"w")
            f.write(name)
            f.close()
            
        if os.path.exists(os.path.join(self.json_folder,"recursive")) == False:
            if recursive == True:
                f = open(os.path.join(self.json_folder,"recursive"),"w")
                f.write("on")
                f.close()
                
        self.reader = None
        self.engine = ""
        self.files_list = []
        self.processed = 0
        self.recursive = recursive
        self.load_files_list(img_folder)
        self.reading = True
        self.current_template_path = ""
        import conf
        self.engines = conf.engines
        
        
    def init_reader(self, engine="dynamsoft"):
        if self.engine == engine:
            return
        self.engine = engine;
        if self.engine == "dynamsoft" or self.engine == "":
            from barcode_reader.dynamsoft import DynamsoftBarcodeReader
            self.reader = DynamsoftBarcodeReader()
        elif self.engine == "DBR 8.8":
            from barcode_reader.commandline import CommandLineBarcodeReader
            self.reader = CommandLineBarcodeReader(port=6666,config_path="dbr88_commandline")
        elif self.engine == "commandline":
            from barcode_reader.commandline import CommandLineBarcodeReader
            self.reader = CommandLineBarcodeReader()
        elif self.engine == "scandit":
            from barcode_reader.commandline import CommandLineBarcodeReader
            self.reader = CommandLineBarcodeReader()
        elif self.engine == "accusoft":
            from barcode_reader.commandline import CommandLineBarcodeReader
            self.reader = CommandLineBarcodeReader(port=5558,config_path="accusoft_commandline")
        elif self.engine == "aspose":
            from barcode_reader.aspose import AsposeBarcodeReader
            self.reader = AsposeBarcodeReader()
        elif self.engine == "zxing":
            from barcode_reader.commandline import CommandLineBarcodeReader
            self.reader = CommandLineBarcodeReader(port=5557, config_path="zxing_commandline")
        elif self.engine == "zxingcpp":
            from barcode_reader.zxingcpp import ZXingBarcodeReader
            self.reader = ZXingBarcodeReader()
        elif self.engine == "zbar":
            from barcode_reader.zbar import ZbarBarcodeReader
            self.reader = ZbarBarcodeReader()
        elif self.engine == "ean13":
            from barcode_reader.ean13 import EAN13Reader
            self.reader = EAN13Reader()
        elif self.engine == "opencv1d":
            from barcode_reader.opencv1d import OpenCV1DReader
            self.reader = OpenCV1DReader()
        elif self.engine == "boofcv":
            from barcode_reader.boofcv import BoofCVReader
            self.reader = BoofCVReader()
        elif self.engine == "opencv_wechat":
            from barcode_reader.opencv_wechat_qrcode import OpenCVWechatQrReader
            self.reader = OpenCVWechatQrReader()
            
    def update_dbr_runtime_settings_if_needed(self, img_path):
        if self.engine == "dynamsoft" or self.engine == "":
            parent_path = os.path.abspath(os.path.join(img_path, os.pardir))
            template_path = os.path.join(parent_path, "template.json")
            if self.current_template_path!=template_path:
                if os.path.exists(template_path):
                    self.current_template_path=template_path
                    f = open(template_path,"r")
                    settings = f.read()
                    f.close()
                    try:
                        self.reader.set_runtime_settings_with_template(settings)
                        print("runtime settings updated")
                    except:
                        print("wrong settings")
                else:
                    self.reader.reset_runtime_settings()
    
    def decode_and_save_results(self):
        self.processed = 0
        for filename in self.files_list:
            print("Decoding "+filename)
            
            if self.reading == False:
                print("Stopped")
                return
            self.update_dbr_runtime_settings_if_needed(os.path.join(self.img_folder,filename))
            start_time = time.time()
            result_dict = {}
            results = []
            try:
                result_dict = self.reader.decode_file(os.path.join(self.img_folder,filename))
            except Exception as e:
                print(e)
            end_time = time.time()
            elapsedTime = int((end_time - start_time) * 1000)
            
            if "results" in result_dict:
                results = result_dict["results"]
            if "elapsedTime" in result_dict:
                elapsedTime = result_dict["elapsedTime"]
            
            json_dict = {}
            json_dict["elapsedTime"] = elapsedTime
            json_dict["results"] = results

            json_string = json.dumps(json_dict, indent="\t")
            self.save_decoding_result(filename,json_string)
            
            self.processed=self.processed+1
            
    def save_decoding_result(self, filename, json_string):
        json_path = os.path.join(self.json_folder,self.get_json_filename(filename))
        parent_path = os.path.abspath(os.path.join(json_path, os.pardir))
        if os.path.exists(parent_path) == False:
            os.makedirs(parent_path)
        f = open(json_path,"w")
        f.write(json_string)
        f.close()
        
    def start_reading(self, engine="dynamsoft"):
        self.init_reader(engine)
        self.reading = True
        if str(self.reader.__class__).find("CommandLine")!=-1:
            self.reader.start_commandline_zmq_server_if_unstarted()
        threading.Thread(target=self.decode_and_save_results, args=()).start()
        
    def stop_reading(self):
        if str(self.reader.__class__).find("CommandLine")!=-1:
            self.reader.stop_commandline_zmq_server_if_started()
        self.reading = False
            
    def load_files_list(self, folder, inner_folder=None):
        for filename in os.listdir(folder):
            path = os.path.join(folder,filename)
            name, ext = os.path.splitext(filename)
            if ext.lower() in ('.png','.jpg','.jpeg','.bmp','.tif', '.tiff','.pdf'):
                if inner_folder!=None:
                    self.files_list.append(os.path.join(inner_folder,filename))
                else:
                    self.files_list.append(filename)
            if os.path.isdir(path) and self.recursive == True:
                self.load_files_list(path, inner_folder=filename)
            
    def get_process(self):
        return "{}/{}".format(self.processed, len(self.files_list))
        
    def completed(self):
        imgs_list = {}
        json_list = {}
        print(self.files_list)
        for filename in self.files_list:
            imgs_list[filename] = ""
            json_filename = self.get_json_filename(filename)
            if os.path.exists(os.path.join(self.json_folder,json_filename)):
                json_list[json_filename] = ""
        for img_filename in imgs_list:
            if self.get_json_filename(img_filename) not in json_list:
                return False
        return True
        
    '''
    Get json name based on image name.
    Image name: 1.jpg
    Json name: 1.jpg.json
    With engine: 1.jpg-engine.json
    '''
    def get_json_filename(self, filename, engine=""):
        if engine=="":
            engine=self.engine
        if engine!="dynamsoft":
            return filename+"-"+engine+".json"
        else:
            return filename+".json"
    
    def get_ground_truth_list(self, filename):
        name, ext = os.path.splitext(filename)
        txt_path = os.path.join(self.img_folder,name+".txt")
        if os.path.exists(txt_path) == False:
            txt_path = os.path.join(self.img_folder,filename+".txt")
        if os.path.exists(txt_path):
            ground_truth_list = []
            try:
                f = open(txt_path, "r")
                content = f.read().strip()
                ground_truth_list=json.loads(content)                
                if isinstance(ground_truth_list,list) == False:
                    ground_truth_list=[]
                    result = {}
                    result["text"] = content
                    ground_truth_list.append(result)
                f.close()
            except Exception as e:
                print(e)
            return ground_truth_list
        return []
    
    def get_statistics(self, engine="dynamsoft", copy_failed=True, files_list=[]):
        print("get statistics of "+engine)
        if len(files_list)==0:
            files_list=self.files_list
        data = {}
        img_results = {}
        total_elapsedTime = 0
        total_images = len(files_list)
        undetected_images = 0
        wrong_detected_images = 0
        
        total_barcodes = 0
        detected_barcodes = 0
        undetected_barcodes = 0
        wrong_detected_barcodes = 0
        
        for filename in files_list:
            
            json_filename = self.get_json_filename(filename, engine)
            json_path = os.path.join(self.json_folder,json_filename)
            failed = False
            if os.path.exists(json_path):
                f = open(json_path,"r",encoding="utf-8")
                image_decoding_result = json.loads(f.read())
                ground_truth_list = self.get_ground_truth_list(filename)
                total_barcodes = total_barcodes + len(ground_truth_list)
                img_results[filename] = image_decoding_result
                
                wrong_detected_of_one_image = 0
                undetected_barcodes_of_one_image = 0
                total_elapsedTime=total_elapsedTime+int(image_decoding_result["elapsedTime"])
                if "results" in image_decoding_result:
                    results=image_decoding_result["results"]
                    if len(results)==0:
                        undetected_images=undetected_images+1
                        undetected_barcodes_of_one_image = len(ground_truth_list)
                        
                        failed = True
                    else:
                        failed, some_detected, undetected_barcodes_of_one_image, wrong_detected_of_one_image = self.is_barcode_correcly_read(results,ground_truth_list)
                        
                        if wrong_detected_of_one_image > 0:
                            image_decoding_result["wrong_detected"] = True
                            wrong_detected_images = wrong_detected_images +1
                        else:
                            if failed == True:
                                undetected_images=undetected_images+1
                        if failed == True and some_detected == True:
                            image_decoding_result["partial_success"] = True
                else:
                    undetected_images=undetected_images+1
                    undetected_barcodes_of_one_image = len(ground_truth_list)
                    failed = True
                    
                image_decoding_result["ground_truth"] = ground_truth_list
                image_decoding_result["undetected_barcodes"] = undetected_barcodes_of_one_image
                image_decoding_result["wrong_detected_barcodes"] = wrong_detected_of_one_image
                
                wrong_detected_barcodes = wrong_detected_barcodes + wrong_detected_of_one_image
                undetected_barcodes = undetected_barcodes + undetected_barcodes_of_one_image
                
                #print("ground truth list")
                #print(ground_truth_list)
                image_decoding_result["failed"] = failed
                if failed == True and copy_failed == True:
                    self.copy_undetected_to_failed_folder(filename, engine)
            else:
                undetected_images = total_images
        self.append_statistics("",total_images,undetected_images,wrong_detected_images, data)
        self.append_statistics("_barcodes",total_barcodes,undetected_barcodes,wrong_detected_barcodes, data)
        data["img_results"] = img_results
        data["time_elapsed"] = total_elapsedTime
        data["average_time"] = total_elapsedTime / total_images
        return data
        
    def append_statistics(self, affix, total, undetected, wrong_detected, data):
        detected = total - undetected
        correctly_detected = detected - wrong_detected
        data["total"+affix] = total
        data["undetected"+affix] = undetected
        data["wrong_detected"+affix] = wrong_detected
        if detected>0:
            precision = correctly_detected / detected
            data["precision"+affix] = precision
        else:
            precision = 0
            data["precision"+affix] = ""
        if total>0:
            accuracy = correctly_detected / total
        else:
            accuracy = 0
            
        data["accuracy"+affix] = accuracy
       
        if precision>0 and accuracy>0:
            data["f1score"+affix] = 2 * (precision * accuracy) / (precision + accuracy)
        else:
            data["f1score"+affix] = 0
    
    def is_barcode_correcly_read(self, results, ground_truth_list):
        failed = False
        barcode_text = ""
        barcodeFormat = ""
        undetected_barcodes = []
        wrong_detected_barcodes = []
        some_detected = False
        for ground_truth in ground_truth_list:
            detected = False
            for result in results:
                if result["y1"] != result["y4"]: # not a line
                    if "x1" in ground_truth: #if there is localization markup
                        detection_points = geometry_utils.points_of_one_detection_result(result)
                        ground_truth_points = geometry_utils.points_of_one_detection_result(ground_truth)
                        iou = geometry_utils.calculate_polygon_iou(detection_points,ground_truth_points)
                        if iou<=0.0: #if not overlapped
                            continue
                correct = self.is_text_correct(result, ground_truth)
                if correct:
                    detected = True
                    some_detected = True
                    break
                else:
                    if result not in wrong_detected_barcodes:
                        wrong_detected_barcodes.append(result)
            if detected == False:
                failed = True
                if ground_truth not in undetected_barcodes:
                    undetected_barcodes.append(ground_truth)
        if len(undetected_barcodes) == 0: #ignore over detected barcodes
            wrong_detected_barcodes = []
        return failed, some_detected, len(undetected_barcodes), len(wrong_detected_barcodes)
        
    def is_text_correct(self, result,ground_truth):
        detected_text = result["barcodeText"].strip()
        ground_truth_text = ground_truth["text"].strip()
        barcodeFormat = result["barcodeFormat"]
        if barcodeFormat.upper().find("UPC") != -1:
            if len(detected_text) == 12:
                detected_text = "0" + detected_text
        if detected_text.find(ground_truth_text) == -1:
            return False
        else:
            return True
    
    def copy_undetected_to_failed_folder(self, filename, engine="dynamsoft"):
        img_path = os.path.join(self.img_folder,filename)
        if engine == "dynamsoft":
            failed_folder_path = os.path.join(self.json_folder,"failed")
        else:
            failed_folder_path = os.path.join(self.json_folder,"failed-" + engine)
        if os.path.exists(failed_folder_path) == False:
            os.mkdir(failed_folder_path)
        target = os.path.join(failed_folder_path,filename)

        parent_path = os.path.abspath(os.path.join(target, os.pardir))
        if os.path.exists(parent_path) == False:
            os.makedirs(parent_path)
        
        copyfile(img_path,target)
        
    
    def get_comparison_in_category(self,include_details=False,engines=None):
        if engines == None:
            engines = self.engines
        result = {}
        files_list_in_category = {}
        for filename in self.files_list:
            category = os.path.dirname(filename)
            files = []
            if category in files_list_in_category:
                files = files_list_in_category[category]
            files.append(filename)
            files_list_in_category[category] = files
        for category in files_list_in_category:
            result[category] = self.get_comparison(include_details=include_details,engines=engines,files_list=files_list_in_category[category])
        return result
    
    def get_comparison(self,include_details=False,engines=None,files_list=[]):
        if len(files_list)==0:
            files_list=self.files_list
        result = {}
        data_dict = {}
        if engines == None:
            engines = self.engines
        for engine in engines:
            data = self.get_statistics(engine=engine,copy_failed=False, files_list=files_list)
            data_dict[engine] = data
            engine_result = {}
            engine_result["precision"] = data["precision"]
            engine_result["accuracy"] = data["accuracy"]
            engine_result["f1score"] = data["f1score"]
            engine_result["precision_barcodes"] = data["precision_barcodes"]
            engine_result["accuracy_barcodes"] = data["accuracy_barcodes"]
            engine_result["f1score_barcodes"] = data["f1score_barcodes"]
            engine_result["time_elapsed"] = data["time_elapsed"]
            engine_result["average_time"] = data["average_time"]
            result[engine] = engine_result
        if include_details:
            self.add_comparison_details(result, data_dict)
        return result
        
    def add_comparison_details(self, result, data_dict):
        img_decoding_details = {}
        for engine in self.engines:
            data = data_dict[engine]
            img_results = data["img_results"]
            for filename in img_results:
                image_decoding_result= img_results[filename]
                detected_list = []
                undetected_list = []
                decoding_details_of_one_img = {}
                if filename in img_decoding_details:
                    decoding_details_of_one_img = img_decoding_details[filename]
                if "detected" in decoding_details_of_one_img:
                    detected_list = decoding_details_of_one_img["detected"]
                if "undetected" in decoding_details_of_one_img:
                    undetected_list = decoding_details_of_one_img["undetected"]
                if image_decoding_result["failed"] == True:
                    undetected_list.append(engine)
                else:
                    detected_list.append(engine)
                decoding_details_of_one_img["detected"] = detected_list
                decoding_details_of_one_img["undetected"] = undetected_list
                img_decoding_details[filename] = decoding_details_of_one_img
        result["mergedDetails"] = img_decoding_details
    
        
        
        
if __name__ == '__main__':
    session = Batch_session("./tmp","./tmp",session_id="c7edc4c5ea9011eb8965e84e068e29b8")
    session.init_reader("commandline")
    if (session.completed()):
        print("Already completed")
        print(session.get_statistics())
    else:
        session.start_reading()
        while session.completed()==False:
            time.sleep(0.2)
            print(session.get_process())
        print("Completed")
    
        