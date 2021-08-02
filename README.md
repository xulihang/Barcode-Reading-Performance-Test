# Barcode Reading Performance Test Tool

This is a tool to test the performance of different barcode reading SDKs. It is designed to test a dataset of barcode images with ground truth. It uses a B/S architecture with Python Flask as its backend.

SDKs included:

1. [Dynamsoft Barcode Reader](https://www.dynamsoft.com/barcode-reader/overview/)
2. [Scandit](https://docs.scandit.com/stable/windows/html/2aca5da4-6f94-43a0-9817-5f413d16f100.htm)
3. [Zxing-cpp](https://github.com/nu-book/zxing-cpp)
4. [Zbar](https://github.com/NaturalHistoryMuseum/pyzbar/)

## Installation

```
pip install -r requirements.txt
```

Optional: 

Some barcode reading SDKs don't provide a Python library. For such cases, we can create a command line tool using the provided SDKs and communicate with the server with [ZeroMQ](https://zeromq.org/).

This is how Scandit is integrated. You can see the example here: <https://github.com/xulihang/BarcodeReader_CommandLine/tree/main/Scandit>

## How to Use

1. Start the server.

    ```
    flask run
    ```

    or:

    ```
    python app.py
    ```

2. Visit <http://127.0.0.1:5000/>. Specify the path of the dataset's folder and create a session.

   The folder should have the images and the txt files which contain the ground truth in JSON format.
   
   An example of the ground truth file:
   
   ```js
   [{"attrib": {"Type": "EAN13"}, "text": "9785699128013", "value_attrib": {}}]
   ```
   
   Every session has a unique ID. We can check them out later with its ID. Previous sessions will be listed on the homepage.
   
   ![](https://raw.githubusercontent.com/xulihang/Barcode-Reading-Performance-Test/main/imgs/homepage.jpg)
   
   You can also assign a name to a session.

3. You will be directed to a session page where you can start decoding with a specified SDK and see the results.

    ![](https://raw.githubusercontent.com/xulihang/Barcode-Reading-Performance-Test/main/imgs/sessionpage.jpg)
    
    There are several metrics: accuracy, precision, elapsed time, average time, etc.
    
    You can also click the image's link to check out the image.
    
    PS: If the ground truth file does not exist and the SDK detected barcodes, the detected one will be considered as correct. If the ground truth is provided, the program will examine whether the ground truth exists in the barcode decoding results.


4. You can compare the results in the comparison page.

   You can list images detected/undetected by some SDK and filter the results. It can also draw a comparison chart.
   
   ![](https://raw.githubusercontent.com/xulihang/Barcode-Reading-Performance-Test/main/imgs/comparisonpage.jpg)
   
   
## Barcode Datasets

There are some existing public datasets available. Scripts to generate ground truth files are provided in the utils folder of this repo.

* [Muenster BarcodeDB](https://www.uni-muenster.de/PRIA/en/forschung/index.shtml)
* [ZVZ-synth & ZVZ-real](https://github.com/abbyy/barcode_detection_benchmark)


