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
        elif self.engine == "scandit":
            from barcode_reader.commandline import CommandLineBarcodeReader
            self.reader = CommandLineBarcodeReader()
        elif self.engine == "zxing":
            from barcode_reader.commandline import CommandLineBarcodeReader
            self.reader = CommandLineBarcodeReader(port=5557,config_path="zxing_commandline")
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
    
    def decode_file(self, file_path,settings=""):
        if settings!="":
            try:
                self.reader.set_runtime_settings_with_template(settings)
            except:
                print("wrong settings")
        return self.reader.decode_file(file_path)
        