#coding=utf-8
from flask import Flask, request, render_template, send_file
from batch_session import Batch_session
import uuid
app = Flask(__name__, static_url_path='/', static_folder='static')

sessions={}

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
            session = Batch_session(img_folder)
            session_id = uuid.uuid1().hex
            sessions[session_id]=session
            return {"status":"success","session_id":session_id}

@app.route('/session/<session_id>/start')
def start_session(session_id):
    if session_id in sessions:
        session = sessions[session_id]
        session.start_reading()
        return "Started"
    else:
        return "Not exist"
   
@app.route('/session/<session_id>/progress')
def get_session_progress(session_id):
    if session_id in sessions:
        session = sessions[session_id]
        return session.get_process()
    else:
        return "Not exist"
   
@app.route('/session/<session_id>/statistics')
def get_session_statistics(session_id):
    if session_id in sessions:
        session = sessions[session_id]
        return ""
    else:
        return "Not exist"

if __name__ == '__main__':
    app.run()
