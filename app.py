#coding=utf-8
from flask import Flask, request, render_template, send_file
from batch_session import Batch_session
import os

app = Flask(__name__, static_url_path='/', static_folder='static')

sessions={}

tmp_path="./tmp"


@app.route('/')
def index():
    return render_template('index.html')
   
@app.route('/session/create', methods=['POST'])
def create_session():
    if request.method == "POST":
        data=request.get_json()
        if "folderpath" in data:
            img_folder = data["folderpath"]
            print(img_folder)
            if os.path.exists(tmp_path) == False:
                os.mkdir(tmp_path)
            session = Batch_session(img_folder,tmp_path)
            session_id = session.get_id()
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
        session = Batch_session(img_folder,tmp_path,session_id=session_id)
        sessions[session_id]=session
    return session

@app.route('/session/<session_id>/start')
def start_session(session_id):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    print(session)
    session.start_reading()
    return "Started"    
   
@app.route('/session/<session_id>/progress')
def get_session_progress(session_id):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    return session.get_process()    

   
@app.route('/session/<session_id>/statistics')
def get_session_statistics(session_id):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    return session.get_statistics()

if __name__ == '__main__':
    app.run()
