from dbr import *
import json
import subprocess
import os
import zmq

class BarcodeReaderX():
    def __init__(self):
        self.dbr = BarcodeReader()
        self.dbr.init_license("t0070fQAAAG16DXrR4sc8gNexDekiNrG6xJSiDAabkbAKOyeFtNASIwCzV+Nc6x1GXNVxyJPapcWE++aFwJYBKTFxNqbunQgbAA==")
        if os.path.exists("template.json"):
            print("Found template")
            self.dbr.init_runtime_settings_with_file("template.json")
        self.context = zmq.Context()
        self.process = None
        self.start_commandline_zmq_server_if_unstarted()

    def start_commandline_zmq_server_if_unstarted(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5556")
        socket.send(b"Hello")
        message = ""
        try:
            message = socket.recv(flags=zmq.NOBLOCK)
        except Exception as e:
            print(e)
            f = open("commandline_path","r")
            commandline_path = f.read()
            f.close()
            self.process = subprocess.Popen([commandline_path.strip()], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
    def stop_commandline_zmq_server_if_started(self):
        try:
            self.process.kill()
        except:
            print("process not opened")
        
    
    def decode_file(self, img_path, engine=""):
        result_dict = {}
        results = []    
        if engine == "":
            text_results = self.dbr.decode_file(img_path)
            
            if text_results!=None:
                for tr in text_results:
                    result = {}
                    result["barcodeFormat"] = tr.barcode_format_string
                    result["barcodeFormat_2"] = tr.barcode_format_string_2
                    result["barcodeText"] = tr.barcode_text
                    bytes_string = ""
                    for i in range(0,len(tr.barcode_bytes)):
                        byte = tr.barcode_bytes[i]
                        hex_data = hex(byte).replace("0x","").upper()
                        if len(hex_data)==1:
                            hex_data = "0" + hex_data
                        hex_data = "00" + hex_data
                        bytes_string= bytes_string + hex_data
                    result["barcodeBytes"] = bytes_string
                    result["confidence"] = tr.extended_results[0].confidence
                    results.append(result)
        elif engine == "commandline":
            try:
                socket = self.context.socket(zmq.REQ)
                socket.connect("tcp://localhost:5556")
                socket.send(bytes(img_path,"utf-8"))
                message = socket.recv()
                json_object = json.loads(message.decode("utf-8"))
                if "results" in json_object:
                    results=json_object["results"]
                if "elapsedTime" in json_object:
                    result_dict["elapsedTime"]=json_object["elapsedTime"]
            except Exception as e:
                print(e)
        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = BarcodeReaderX()
    results = reader.decode_file("D:\\test\\BarcodePerformance\\test.jpg")
    print(results)
    