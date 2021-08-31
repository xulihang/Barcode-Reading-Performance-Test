import cv2

class OpenCVWechatQrReader():
    def __init__(self):
        self.detector = cv2.wechat_qrcode_WeChatQRCode("detect.prototxt", "detect.caffemodel", "sr.prototxt", "sr.caffemodel")

    def decode_file(self, img_path):
        result_dict = {}
        results = []
        img = cv2.imread(img_path)
        res, points = self.detector.detectAndDecode(img)
        for i in range(len(res)):
            result = {}
            result["barcodeFormat"] = "QR"
            result["barcodeText"] = res[i]
            vertex = points[i]
            result["x1"] = int(vertex[0][0])
            result["y1"] = int(vertex[0][1])
            result["x2"] = int(vertex[1][0])
            result["y2"] = int(vertex[1][1])
            result["x3"] = int(vertex[2][0])
            result["y3"] = int(vertex[2][1])
            result["x4"] = int(vertex[3][0])
            result["y4"] = int(vertex[3][1])
            results.append(result)

        result_dict["results"] = results
        return result_dict
        
if __name__ == '__main__':
    reader = OpenCVWechatQrReader()
    results = reader.decode_file("test.jpg")
    print(results)
    