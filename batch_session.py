#coding=utf-8
import json
import os
import time
import threading
import uuid
from shutil import copyfile

class Batch_session():
    def __init__(self, img_folder, output_folder, template=None,session_id=None, name=""):
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
        
        self.reader = None
        self.engine = ""
        self.files_list = []
        self.processed = 0
        self.load_files_list()
        self.reading = True
        self.engines = ["dynamsoft","commandline","zxing","zbar"]
        
        
    def init_reader(self, engine="dynamsoft"):
        if self.engine == engine:
            return
        self.engine = engine;
        if self.engine == "dynamsoft" or self.engine == "":
            from barcode_reader.dynamsoft import DynamsoftBarcodeReader
            self.reader = DynamsoftBarcodeReader()
        elif self.engine == "commandline":
            from barcode_reader.commandline import CommandLineBarcodeReader
            self.reader = CommandLineBarcodeReader()
        elif self.engine == "zxing":
            from barcode_reader.zxing import ZXingBarcodeReader
            self.reader = ZXingBarcodeReader()
        elif self.engine == "zbar":
            from barcode_reader.zbar import ZbarBarcodeReader
            self.reader = ZbarBarcodeReader()    
            
    
    def decode_and_save_results(self):
        self.processed = 0
        for filename in self.files_list:
            print("Decoding "+filename)
            if self.reading == False:
                print("Stopped")
                return
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
            
            f = open(os.path.join(self.json_folder,self.get_json_filename(filename)),"w")
            f.write(json_string)
            f.close()
            self.processed=self.processed+1
            
    def start_reading(self, engine="dynamsoft"):
        self.init_reader(engine)
        self.reading = True
        if self.engine == "commandline":
            self.reader.start_commandline_zmq_server_if_unstarted()
        threading.Thread(target=self.decode_and_save_results, args=()).start()
        
    def stop_reading(self):
        if self.engine == "commandline":
            self.reader.stop_commandline_zmq_server_if_started()
        self.reading = False
            
    def load_files_list(self):
        for filename in os.listdir(self.img_folder):
            name, ext = os.path.splitext(filename)
            if ext.lower() in ('.png','.jpg','.jpeg','.bmp','.tif', '.tiff','.pdf'):
                self.files_list.append(filename)

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
    
    def get_statistics(self, engine="dynamsoft", copy_failed=True):
        data = {}
        img_results = {}
        total_elapsedTime = 0
        undetected = 0
        wrong_detected = 0
        
        for filename in self.files_list:
            json_filename = self.get_json_filename(filename, engine)
            json_path = os.path.join(self.json_folder,json_filename)
            if os.path.exists(json_path):
                failed = False
                f = open(json_path,"r",encoding="utf-8")
                image_decoding_result = json.loads(f.read())
                ground_truth_list = self.get_ground_truth_list(filename)
                img_results[filename] = image_decoding_result
                if "results" in image_decoding_result:
                    results=image_decoding_result["results"]
                    if len(results)==0:
                        undetected=undetected+1
                        failed = True
                    else:
                        barcode_text = ""
                        for result in results:
                            barcode_text = barcode_text + " " + result["barcodeText"]
                        total_elapsedTime=total_elapsedTime+int(image_decoding_result["elapsedTime"])
                        
                        some_detected = False
                        for ground_truth in ground_truth_list:
                            text = ground_truth["text"].strip()
                            if barcode_text.find(text) == -1:
                                wrong_detected=wrong_detected+1
                                image_decoding_result["wrong_detected"] = True
                                failed = True
                            else:
                                some_detected = True
                        if failed == True and some_detected == True:
                            image_decoding_result["partial_success"] = True
                else:
                    undetected=undetected+1
                    failed = True
                    
                image_decoding_result["ground_truth"] = ground_truth_list
                #print("ground truth list")
                #print(ground_truth_list)
                image_decoding_result["failed"] = failed
                if failed == True and copy_failed == True:
                    self.copy_undetected_to_failed_folder(filename, engine)
                
        total = len(self.files_list)
        detected = total - undetected
        correctly_detected = detected - wrong_detected
        data["img_results"] = img_results
        data["total"] = total
        data["undetected"] = undetected
        data["wrong_detected"] = wrong_detected
        if detected>0:
            data["precision"] = correctly_detected / detected
        else:
            data["precision"] = ""
        data["accuracy"] = correctly_detected / total
        data["time_elapsed"] = total_elapsedTime
        data["average_time"] = total_elapsedTime / total
        return data
        
    def copy_undetected_to_failed_folder(self, filename, engine="dynamsoft"):
        img_path = os.path.join(self.img_folder,filename)
        if engine == "dynamsoft":
            failed_folder_path = os.path.join(self.json_folder,"failed")
        else:
            failed_folder_path = os.path.join(self.json_folder,"failed-" + engine)
        if os.path.exists(failed_folder_path) == False:
            os.mkdir(failed_folder_path)
        target = os.path.join(failed_folder_path,filename)
        copyfile(img_path,target)
        
    def get_comparison(self,include_details=False):
        result = {}
        data_dict = {}
        for engine in self.engines:
            data = self.get_statistics(engine=engine,copy_failed=False)
            data_dict[engine] = data
            engine_result = {}
            engine_result["precision"] = data["precision"]
            engine_result["accuracy"] = data["accuracy"]
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
    
        