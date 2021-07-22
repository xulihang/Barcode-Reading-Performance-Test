from dbr import *
from subprocess import Popen, PIPE, STDOUT
import json

class BarcodeReaderX():
    def __init__(self):
        self.dbr = BarcodeReader()
        self.dbr.init_license("t0069fQAAADni8mnJeS0cnoLp85KEXFCh78ltXDT3x52OWWW0qsnvVBOkG7nz+do12XxdqoHCJQ+U+Bbg+RPP/7nyQsQkDtOC")
    
    def decode_file(self, img_path, engine=""):
        results = []        
        if engine == "":
            text_results = self.dbr.decode_file(img_path)
            if text_results!=None:
                for tr in text_results:
                    result = {}
                    result["barcodeFormat"] = tr.barcode_format_string
                    result["barcodeText"] = tr.barcode_text
                    result["confidence"] = tr.extended_results[0].confidence
                    results.append(result)
        elif engine == "commandline":
            try:
                f = open("commandline_path","r")
                commandline_path = f.read()
                f.close()
                p = Popen([commandline_path.strip(), img_path.strip()], stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                #output = p.stdout.read()
                output = p.communicate()[0]
                print(output)
                json_object = json.loads(output)
                if "results" in json_object:
                    results=json_object["results"]
                p.kill()
            except:
                print("Error")
        return results
        
if __name__ == '__main__':
    reader = BarcodeReaderX()
    results = reader.decode_file("./test.jpg", engine="commandline")
    print(results)
    