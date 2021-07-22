#coding=utf-8
from dbr import *
import json
import os
import time
import _thread
import uuid

class Batch_session():
    def __init__(self, img_folder, output_folder, template=None,session_id=None):
        self.img_folder = img_folder
        self.output_folder = output_folder
        self.id = uuid.uuid1().hex
        
        if session_id != None:
            self.id = session_id
        self.json_folder = os.path.join(self.output_folder,self.id)
        if os.path.exists(self.json_folder) == False:
            os.mkdir(self.json_folder)
            
        f = open(os.path.join(self.json_folder,"img_folder"),"w")
        f.write(img_folder)
        f.close()
        
        self.files_list = []
        self.processed = 0
        self.reader = BarcodeReader()
        self.reader.init_license("t0069fQAAADni8mnJeS0cnoLp85KEXFCh78ltXDT3x52OWWW0qsnvVBOkG7nz+do12XxdqoHCJQ+U+Bbg+RPP/7nyQsQkDtOC")
        self.load_files_list()
    
    def get_id(self):
        return self.id
    
    def decode_and_save_results(self):
        self.processed = 0
        for filename in self.files_list:
            
            start_time = time.time()
            text_results = None
            try:
                text_results = self.reader.decode_file(os.path.join(self.img_folder,filename))
            except:
                print("Error")
            end_time = time.time()
            json_dict = {}
            results = []
            index=0
            if text_results!=None:
                for tr in text_results:
                    result = {}
                    result["barcodeFormat"] = tr.barcode_format_string
                    result["barcodeText"] = tr.barcode_text
                    result["confidence"] = tr.extended_results[0].confidence
                    results.append(result)
                    index=index+1
            json_dict["elapsedTime"] = int((end_time - start_time) * 1000)
            json_dict["results"] = results
            json_string = json.dumps(json_dict, indent="\t")
            
            f = open(os.path.join(self.json_folder,filename+".json"),"w")
            f.write(json_string)
            f.close()
            self.processed=self.processed+1
            
    def start_reading(self, engine=""):
        _thread.start_new_thread(self.decode_and_save_results,())
            
    def load_files_list(self):
        for filename in os.listdir(self.img_folder):
            name, ext = os.path.splitext(filename)
            if ext.lower() in ('.png','.jpg','.jpeg','.bmp'):
                self.files_list.append(filename)

    def get_process(self):
        return "{}/{}".format(self.processed, len(self.files_list))
        
    def completed(self, engine=""):
        imgs_list = {}
        json_list = {}

        for filename in self.files_list:
            imgs_list[filename] = ""
            json_filename = self.get_json_filename(filename, engine)
            if os.path.exists(os.path.join(self.json_folder,json_filename)):
                json_list[json_filename] = ""
        for img_filename in imgs_list:
            if self.get_json_filename(img_filename,engine) not in json_list:
                return False
        return True
        
    '''
    Get json name based on image name.
    Image name: 1.jpg
    Json name: 1.jpg.json
    With engine: 1.jpg-engine.json
    '''
    def get_json_filename(self, filename, engine=""):
        if engine!="":
            return filename+"-"+engine+".json"
        else:
            return filename+".json"
    
    def get_ground_truth(self, filename):
        return filename.split("-")[0]
    
    def get_statistics(self, engine=""):
        data = {}
        img_results = {}
        total_elapsedTime = 0
        undetected = 0
        wrong_detected = 0
        
        for filename in self.files_list:
            json_filename = self.get_json_filename(filename, engine)
            json_path = os.path.join(self.json_folder,json_filename)
            if os.path.exists(json_path):
                print(json_path)
                f = open(json_path,"r",encoding="utf-8")
                image_decoding_result = json.loads(f.read())
                img_results[filename] = image_decoding_result
                if "results" in image_decoding_result:
                    results=image_decoding_result["results"]
                    if len(results)==0:
                        undetected=undetected+1
                    else:
                        ground_truth = self.get_ground_truth(filename)
                        for result in results:
                            barcode_text = result["barcodeText"]
                        total_elapsedTime=total_elapsedTime+int(image_decoding_result["elapsedTime"])
                        if ground_truth!=barcode_text:
                            wrong_detected=wrong_detected+1
                else:
                    undetected=undetected+1
        total = len(self.files_list)
        correctly_detected = total - undetected - wrong_detected
        data["img_results"] = img_results
        data["total"] = total
        data["undetected"] = undetected
        data["wrong_detected"] = wrong_detected
        
        data["precision"] = correctly_detected / (total - undetected)
        data["accuracy"] = correctly_detected / total
        data["time_elapsed"] = total_elapsedTime
        data["average_time"] = total_elapsedTime / total
        return data
        
        
if __name__ == '__main__':
    session = Batch_session("./","./tmp",session_id="c7edc4c5ea9011eb8965e84e068e29b8")
    if (session.completed()):
        print("Already completed")
        print(session.get_statistics())
    else:
        session.start_reading()
        while session.completed()==False:
            time.sleep(0.2)
            print(session.get_process())
        print("Completed")
    
        