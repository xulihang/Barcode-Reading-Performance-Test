import decode as decoder
import detect as detector
import cv2

if __name__ == "__main__":    
    image = cv2.imread("05102009158.jpg")
    candidates = detector.detect(image)
    for i in range(len(candidates)):
        candidate = candidates[i]
        cropped = candidate["cropped"]
        rect = candidate["rect"]
        ean13, is_valid, thresh = decoder.decode(cropped)
        if is_valid:
            text = "Code: " + ean13
            top = thresh.shape[0]-20
            print(top)
            cv2.putText(thresh, text, (5,top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            cv2.imshow(str(i), thresh);
    cv2.waitKey(0);
    cv2.destroyAllWindows();
