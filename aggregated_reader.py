class AggregatedReader():

    def __init__(self, engine="dynamsoft"):
        self.reader = None
        self.engine = engine
        self.init_reader()
        
    def init_reader(self):
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
            
    def decode_file(self, file_path):
        return self.reader.decode_file(file_path)