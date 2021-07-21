#coding=utf-8
from dbr import *
import json
import os
import time
import _thread

class Batch_session():
    def __init__(self, img_folder, template=None):
        self.img_folder = img_folder
        self.files_list = []
        self.processed = 0
        self.reader = BarcodeReader()
        self.reader.init_license("t0069fQAAADni8mnJeS0cnoLp85KEXFCh78ltXDT3x52OWWW0qsnvVBOkG7nz+do12XxdqoHCJQ+U+Bbg+RPP/7nyQsQkDtOC")
        self.load_files_list()
    
    def decode_and_save_results(self):
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
            f = open(os.path.join(self.img_folder,filename+".json"),"w")
            f.write(json_string)
            f.close()
            self.processed=self.processed+1
            
    def start_reading(self):
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
        for filename in os.listdir(self.img_folder):
            name, ext = os.path.splitext(filename)
            if ext.lower() in ('.png','.jpg','.jpeg','.bmp'):
                imgs_list[filename] = ""
                json_filename = self.get_json_filename(filename, engine)
                if os.path.exists(os.path.join(self.img_folder,json_filename)):
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
            
    def get_statistics():
        return ""
        
        
if __name__ == '__main__':
    session = Batch_session("./")
    if (session.completed()):
        print("Already completed")
    else:
        session.start_reading()
        while session.completed()==False:
            time.sleep(0.2)
            print(session.get_process())
        print("Completed")
    
        