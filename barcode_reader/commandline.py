import json
import subprocess
import os
import zmq

class CommandLineBarcodeReader():
    def __init__(self, config_path="scandit_commandline",port=5556):
        self.context = zmq.Context()
        self.process = None
        self.config_path = config_path
        self.port = port
        self.start_commandline_zmq_server_if_unstarted()
        

    def start_commandline_zmq_server_if_unstarted(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://localhost:"+str(self.port))
        socket.send(b"Hello")
        message = ""
        try:
            message = socket.recv(flags=zmq.NOBLOCK)
            print(message)
        except Exception as e:
            print("start error")
            print(e)
            f = open(self.config_path,"r")
            commandline=[]
            for line in f.readlines():
                commandline.append(line.strip())
            f.close()
            self.process = subprocess.Popen(commandline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
    def stop_commandline_zmq_server_if_started(self):
        try:
            self.process.kill()
        except:
            print("process not opened")
        
    
    def decode_file(self, img_path):
        result_dict = {}
        results = []
        try:
            socket = self.context.socket(zmq.REQ)
            socket.connect("tcp://localhost:"+str(self.port))
            socket.send(bytes(img_path,"utf-8"))
            message = socket.recv()
            json_object = json.loads(message.decode("utf-8"))
            if "results" in json_object:
                results=json_object["results"]
            if "elapsedTime" in json_object:
                result_dict["elapsedTime"]=json_object["elapsedTime"]
        except Exception as e:
            print("decode error")
            print(e)
        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    #reader = CommandLineBarcodeReader()
    #reader = CommandLineBarcodeReader(config_path="zxing_commandline",port=5557)
    reader = CommandLineBarcodeReader(config_path="dbr88_commandline",port=6666)
    
    results = reader.decode_file("D:\\test\\BarcodePerformance\\new\\black_qr_code.png")
    print(results)
    reader.stop_commandline_zmq_server_if_started()
    