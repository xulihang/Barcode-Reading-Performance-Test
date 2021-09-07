#coding=utf-8
from flask import Flask, request, render_template, send_file
from batch_session import Batch_session
import aggregated_reader
import os
import base64
import uuid
import cv2
import numpy as np
import io
import sys
import pyboof as pb

print(sys.path.append('./barcode_reader'))

app = Flask(__name__, static_url_path='/', static_folder='static')

sessions={}

reader = aggregated_reader.AggregatedReader()

tmp_path="./tmp"

if os.path.exists(tmp_path)==False:
    os.mkdir("tmp")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/session/<session_id>/image/<filename>')    
def get_image(session_id, filename):
    path = get_image_path(session_id, filename)
    if os.path.exists(path):
        return send_file(path)
    else:
        return "Not exist"
        
@app.route('/session/<session_id>/image_path/<filename>')   
def get_image_path(session_id, filename):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    img_folder = session.img_folder
    return os.path.join(img_folder,filename)
    
@app.route('/session/<session_id>/jpg/<filename>')
def get_image_as_jpg(session_id, filename):
    path = get_image_path(session_id, filename)
    if os.path.exists(path):
        img = cv2.imread(path)
        jpg = cv2.imencode('.jpg', img)[1]
        #image_code = str(base64.b64encode(jpg))[2:-1]
        return send_file(io.BytesIO(jpg), mimetype='image/jpeg')
    else:
        return "Not exist"
        
@app.route('/convert_base64', methods=['POST'])
def convert_base64():
    data=request.get_json()
    imgData = base64.b64decode(data["base64"])
    nparr = np.fromstring(imgData, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = cv2.imencode('.jpg', img_np)[1]
    base64_data = str(base64.b64encode(image))[2:-1]
    return base64_data
   
@app.route('/session/create', methods=['POST'])
def create_session():
    if request.method == "POST":
        data=request.get_json()
        if "folderpath" in data:
            img_folder = data["folderpath"]
            session_name = ""
            recursive = False
            if "name" in data:
                session_name = data["name"]
            
            if "recursive" in data:
                if data["recursive"] == "enabled":
                    recursive = True
                    
            if os.path.exists(tmp_path) == False:
                os.mkdir(tmp_path)
            session = Batch_session(img_folder,tmp_path,name=session_name,recursive=recursive)
            session_id = session.id
            sessions[session_id]=session
            return {"status":"success","session_id":session_id}

def get_session(session_id):
    session = None
    if session_id in sessions:
        session = sessions[session_id]
    elif os.path.exists(os.path.join(tmp_path,session_id))==True:
        session_folder = os.path.join(tmp_path,session_id)
        f = open(os.path.join(session_folder,"img_folder"),"r")
        img_folder = f.read()
        f.close()
        recursive = False
        if os.path.exists(os.path.join(session_folder,"recursive")):
            recursive = True    
        session = Batch_session(img_folder,tmp_path,session_id=session_id,recursive=recursive)
        sessions[session_id]=session
    return session

@app.route('/session/<session_id>/start/<engine>')
def start_session(session_id, engine):
    session = get_session(session_id)
    if session == None:
        return "Not exist"    
    session.start_reading(engine=process_engine(engine))
    return "Started"
    
@app.route('/session/<session_id>/stop/<engine>')
def stop_session(session_id, engine):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    session.stop_reading()
    return "Stopped"
   
@app.route('/session/<session_id>/progress')
def get_session_progress(session_id):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    return session.get_process()    

@app.route('/session/<session_id>/statistics/<engine>')
def get_session_statistics(session_id, engine):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    return session.get_statistics(engine=process_engine(engine))
    
def process_engine(engine):
    if engine == "":
        return "dynamsoft"
    else:
        return engine

@app.route('/session/<session_id>/comparison/', methods=['POST'])
def get_session_comparison(session_id):
    if request.method == "POST":
        data=request.get_json(force=True)
        engines = None
        in_category = False
        if data!=None:
            if "engines" in data:
                engines = data["engines"]
            if "in_category" in data:
                in_category = True
        session = get_session(session_id)
        if session == None:
            return "Not exist"
        if in_category:
            return session.get_comparison_in_category(engines=engines)
        else:
            return session.get_comparison(engines=engines)
    
@app.route('/session/<session_id>/complete-comparison/')
def get_session_complete_comparison(session_id):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    return session.get_comparison(include_details=True)
        
@app.route('/session/list/')
def get_session_list():
    sessions_dict = {}
    for filename in os.listdir(tmp_path):
        session_dir = os.path.join(tmp_path,filename)
        img_folder_conf = os.path.join(session_dir,"img_folder")
        name_conf = os.path.join(session_dir,"name")
        if os.path.exists(img_folder_conf):
            f = open(img_folder_conf,"r")
            folder_path = f.read()
            f.close()
            sessions_dict[filename] = folder_path
            if os.path.exists(name_conf):
                f = open(name_conf,"r")
                sessions_dict[filename] = sessions_dict[filename] +":"+f.read();
                f.close()
            
    return sessions_dict

@app.route('/session/<session_id>/ground_truth/<filename>')
def get_ground_truth(session_id, filename):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    ground_truth_list = session.get_ground_truth_list(filename)
    result = {}
    result["ground_truth"] = ground_truth_list
    return result
    
@app.route('/engines')
def get_engines():
    import conf
    result={}
    result["engines"] = conf.engines
    return result

@app.route('/decode', methods=['POST'])
def decode():
    data = request.get_json()
    engine = data["engine"]
    reader.engine = engine
    reader.init_reader()
    settings = ""
    if "settings" in data:
        settings = data["settings"]
    if "base64" in data:
        image_data = base64.b64decode(data["base64"])
        path = uuid.uuid1().hex
        file = open(path,'wb')
        file.write(image_data)
        file.close()
        results = reader.decode_file(os.path.abspath(path),settings=settings)
        os.remove(path)
        return results
    elif "session_id" in data:
        session_id = data["session_id"]
        filename = data["filename"]
        return reader.decode_file(get_image_path(session_id,filename),settings=settings)
    else:
        return "No valid data"
        
    
    
    
    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5111)
