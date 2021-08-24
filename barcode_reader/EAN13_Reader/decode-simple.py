import cv2

def decode(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("gray.jpg",gray)
    #ret, thresh =cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    ret, thresh =cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("thresh.jpg",thresh)
    thresh = cv2.bitwise_not(thresh)
    ean13 = None
    is_valid = None
    #scan lines
    line = thresh[int(img.shape[0]/2)]
    
    #read_bars(line)
    ean13, is_valid = decode_line(line)

    return ean13, is_valid, thresh
            
def read_bars(line):
    replace_255_to_1(line)
    bars = []
    current_length = 1
    for i in range(len(line)-1):
        if line[i] == line[i+1]:
            current_length = current_length + 1
        else:
            bars.append(current_length * str(line[i]))
            current_length = 1
    #remove quite zone
    bars.pop(0)
    return bars
    
def detect_module_size(bars):
    size = len(bars[0])
    for bar in bars:
        size = min(len(bar),size)
    return size
    
def decode_line(line):
    replace_255_to_1(line)
    print(line)
    module_size = detect_module_size(read_bars(line))
    data_string = array_as_string(line,module_size)
    guard_pattern = "101"
    center_guard_pattern = "01010"

    begin_index = data_string.find(guard_pattern)+len(guard_pattern)
    data_string_left = data_string[begin_index:-1]

    left_codes = []
    for i in range(6):
        start_index = i*7
        bar_pattern = data_string_left[start_index:start_index+7]
        decoded = decode_left_bar_pattern(bar_pattern)
        print(decoded)
        left_codes.append(decoded)

    data_string_left = data_string_left[6*7:-1]
    
    center_index = data_string_left.find(center_guard_pattern)+len(center_guard_pattern)
    data_string_left = data_string_left[center_index:-1]

    right_codes = []
    for i in range(6):
        start_index = i*7
        bar_pattern = data_string_left[start_index:start_index+7]
        decoded = decode_right_bar_pattern(bar_pattern)
        print(decoded)
        right_codes.append(decoded)
    
    ean13 = get_ean13(left_codes,right_codes)
    print("Decoded code: " + ean13)
    is_valid = verify(ean13)
    return ean13, is_valid

def verify(ean13):
    weight = [1,3,1,3,1,3,1,3,1,3,1,3,1,3]
    weighted_sum = 0
    for i in range(12):
        weighted_sum = weighted_sum + weight[i] * int(ean13[i])
    weighted_sum = str(weighted_sum)
    checksum = 0
    units_digit = int(weighted_sum[-1])
    if units_digit != 0:
        checksum = 10 - units_digit
    else:
        checksum = 0
    print("The checksum of "+ean13 + " is " + str(checksum))
    if checksum == int(ean13[-1]):
        print("The code is valid.")
        return True
    else:
        print("The code is invalid.")
        return False

def get_ean13(left_codes,right_codes):
    ean13 = ""
    ean13 = ean13 + str(get_first_digit(left_codes))
    for code in left_codes:
        ean13 = ean13 + str(code["code"])
    for code in right_codes:
        ean13 = ean13 + str(code["code"])
    return ean13
    
def array_as_string(array, module_size):
    s = ""
    for value in array:
        s = s + str(value)
    s=s.replace("1"*module_size,"1")
    s=s.replace("0"*module_size,"0")
    print("Data string: " + s)
    return s
    
def replace_255_to_1(array):
    for i in range(len(array)):
        if array[i] == 255:
            array[i] = 1

    
def decode_left_bar_pattern(pattern):
    left_pattern_dict = {}
    left_pattern_dict["0001101"] = {"code":0,"parity":"O"}
    left_pattern_dict["0100111"] = {"code":0,"parity":"E"}
    left_pattern_dict["0011001"] = {"code":1,"parity":"O"}
    left_pattern_dict["0110011"] = {"code":1,"parity":"E"}
    left_pattern_dict["0010011"] = {"code":2,"parity":"O"}
    left_pattern_dict["0011011"] = {"code":2,"parity":"E"}
    left_pattern_dict["0111101"] = {"code":3,"parity":"O"}
    left_pattern_dict["0100001"] = {"code":3,"parity":"E"}
    left_pattern_dict["0100011"] = {"code":4,"parity":"O"}
    left_pattern_dict["0011101"] = {"code":4,"parity":"E"}
    left_pattern_dict["0110001"] = {"code":5,"parity":"O"}
    left_pattern_dict["0111001"] = {"code":5,"parity":"E"}
    left_pattern_dict["0101111"] = {"code":6,"parity":"O"}
    left_pattern_dict["0000101"] = {"code":6,"parity":"E"}
    left_pattern_dict["0111011"] = {"code":7,"parity":"O"}
    left_pattern_dict["0010001"] = {"code":7,"parity":"E"}
    left_pattern_dict["0110111"] = {"code":8,"parity":"O"}
    left_pattern_dict["0001001"] = {"code":8,"parity":"E"}
    left_pattern_dict["0001011"] = {"code":9,"parity":"O"}
    left_pattern_dict["0010111"] = {"code":9,"parity":"E"}
    return left_pattern_dict[pattern]
    
def decode_right_bar_pattern(pattern):
    right_pattern_dict = {}
    right_pattern_dict["1110010"] = {"code":0}
    right_pattern_dict["1100110"] = {"code":1}
    right_pattern_dict["1101100"] = {"code":2}
    right_pattern_dict["1000010"] = {"code":3}
    right_pattern_dict["1011100"] = {"code":4}
    right_pattern_dict["1001110"] = {"code":5}
    right_pattern_dict["1010000"] = {"code":6}
    right_pattern_dict["1000100"] = {"code":7}
    right_pattern_dict["1001000"] = {"code":8}
    right_pattern_dict["1110100"] = {"code":9}
    return right_pattern_dict[pattern]

def get_first_digit(left_codes):
    parity_dict = {}
    parity_dict["OOOOOO"] = 0
    parity_dict["OOEOEE"] = 1
    parity_dict["OOEEOE"] = 2
    parity_dict["OOEEEO"] = 3
    parity_dict["OEOOEE"] = 4
    parity_dict["OEEOOE"] = 5
    parity_dict["OEEEOO"] = 6
    parity_dict["OEOEOE"] = 7
    parity_dict["OEOEEO"] = 8
    parity_dict["OEEOEO"] = 9
    parity = ""
    for code in left_codes:
        parity = parity + code["parity"]
    return parity_dict[parity]
    

if __name__ == "__main__":
    img = cv2.imread("generated.jpg")
    ean13, is_valid, thresh = decode(img)
    cv2.imshow("title", thresh);
    cv2.waitKey(0);
    cv2.destroyAllWindows();

