import cv2
import numpy as np


def detect(img):
    scale_percent = 640/img.shape[1]       
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) #normalize
    
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    ret, thresh =cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #ret, thresh =cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.bitwise_not(thresh)
    kernel = np.ones((3, 20), np.uint8)
    thresh = cv2.dilate(thresh, kernel)
    #thresh = cv2.erode(thresh, kernel)
    #thresh = cv2.erode(thresh, kernel)

    original_sized = cv2.resize(thresh, (img.shape[1],img.shape[0]), interpolation = cv2.INTER_AREA)
    #cv2.imwrite("dilated.jpg",original_sized)
    contours, hierarchy = cv2.findContours(original_sized,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    
    
    candidates = []
    index = 0
    added_index = []
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect) 
        box = np.int0(box)
        #area = cv2.contourArea(cnt)
        cropped = crop_rect(rect,box,img)
        width = cropped.shape[1]
        child_index = hierarchy[0][index][2]
        parent_index = hierarchy[0][index][3]
        #the min width of EAN13 is 95 pixel
        if width>95:
            #print("current_index: "+str(index))
            has_overlapped = False
            if child_index in added_index:
                has_overlapped = True
            #if parent_index in added_index:
            #    has_overlapped = True
            if has_overlapped == False:
                added_index.append(index)
                candidate = {"cropped": cropped, "rect": rect}
                candidates.append(candidate)
        index = index + 1
    return candidates

def crop_rect(rect, box, img):
    W = rect[1][0]
    H = rect[1][1]
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
     
     
    # Center of rectangle in source image
    center = ((x1+x2)/2,(y1+y2)/2)
    # Size of the upright rectangle bounding the rotated rectangle
    size = (x2-x1, y2-y1)
    # Cropped upright rectangle
    cropped = cv2.getRectSubPix(img, size, center)
    
    
    angle = rect[2]
    if angle!=90: #need rotation
        if angle>45:
            angle = 0 - (90 - angle)
        else:
            angle = angle
        #print(angle)

        M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)
        
        cropped = cv2.warpAffine(cropped, M, size)
        croppedW = H if H > W else W
        croppedH = H if H < W else W
        # Final cropped & rotated rectangle
        croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW),int(croppedH)), (size[0]/2, size[1]/2))
        return croppedRotated
    return cropped


if __name__ == "__main__":    
    image = cv2.imread("multiple.jpg")
    candidates = detect(image)
    for i in range(len(candidates)):
        candidate = candidates[i]
        cv2.imshow(str(i), candidate["cropped"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
