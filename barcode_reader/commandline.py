import json
import subprocess
import os
import zmq

class CommandLineBarcodeReader():
    def __init__(self):
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
            print(commandline_path)
            self.process = subprocess.Popen([commandline_path.strip()], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
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
    reader = CommandLineBarcodeReader()
    results = reader.decode_file("D:\\test\\BarcodePerformance\\test.jpg")
    print(results)
    