import decode as decoder
import detect as detector
import cv2
import numpy as np

if __name__ == "__main__":    
    image = cv2.imread("multiple.jpg")
    candidates = detector.detect(image)
    text = "No barcode found"
    for i in range(len(candidates)):
        candidate = candidates[i]
        cropped = candidate["cropped"]
        rect = candidate["rect"]
        box = cv2.boxPoints(rect) 
        box = np.int0(box)
        ean13, is_valid, thresh = decoder.decode(cropped)
        if is_valid:
            if text == "No barcode found":
                text = "Code: "
            text = text + ean13 + " "
            cv2.line(image,(box[0][0],box[0][1]),(box[1][0],box[1][1]),(0,255,0),3)
            cv2.line(image,(box[1][0],box[1][1]),(box[2][0],box[2][1]),(0,255,0),3)
            cv2.line(image,(box[2][0],box[2][1]),(box[3][0],box[3][1]),(0,255,0),3)
            cv2.line(image,(box[3][0],box[3][1]),(box[0][0],box[0][1]),(0,255,0),3)
    scale_percent = 640/image.shape[1]       
    width = int(image.shape[1] * scale_percent)
    height = int(image.shape[0] * scale_percent)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    cv2.putText(resized, text, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.imshow(str(i), resized);
    cv2.waitKey(0);
    cv2.destroyAllWindows();
