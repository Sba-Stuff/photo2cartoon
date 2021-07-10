# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import *
import sys
import os
import cv2
from werkzeug import secure_filename
import re
import random

#TEMPLATE_DIR = os.path.abspath('../templates')
#STATIC_DIR = os.path.abspath('../static')
# app = Flask(__name__) # to make the app run without any
#app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {"png","jpg","jpeg"}
app = Flask(__name__,template_folder="template/",static_folder="static/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#@app.route('/output/<path:filepath>')
#def stater(filepath):
#    return send_from_directory('output', filepath)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def htmloader(text,inputaudio,outputaudio):
    x = ""
    x+="Utterance: <p>"+text+"</p><br>"
    x+="Original:<br>"
    x+="<audio controls>"
    x+="  <source src='"+inputaudio+"' type='audio/"+inputaudio.rsplit('.', 1)[1].lower()+"'>"
    x+="</audio><br>"
    x+="Cloned Utterance:<br>"
    x+="<audio controls>"
    x+="  <source src='"+str(outputaudio)+"' type='audio/wav'>"
    x+="</audio><br>"
    return x

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def upload_file():
    fil = []
    if request.method == 'POST':
        f = request.files['file']
        if allowed_file(f.filename):
            f.save(UPLOAD_FOLDER+secure_filename("test.jpg"))
            fil.append("File uploaded successfully")
            fil.append(UPLOAD_FOLDER+secure_filename(f.filename))
            return fil
        else:
            fil.append("Not An Expected File")
            return fil
@app.route('/',methods=['GET', 'POST'])
def hello_world():
    legoutput = upload_file()
    lig = "This is a demo utterance. This will work when you do not add any utterance."
    if request.method == 'POST':
        print(str(lig))
    #return mainpage()
    if str(legoutput)=="None":
        return render_template("index.html",output="Please Upload A Valid File. Dimagh Na Kha.")
    else:
        codehtml = "<b>Original:</b></br><img src='static/test.jpg' height='293' width='453'></br>Cartoon:</b></br><img src='static/cartoon-test.jpg' height='293' width='453'></br>"
        from p2cgencore import Photo2Cartoon
        img = cv2.cvtColor(cv2.imread("static/test.jpg"), cv2.COLOR_BGR2RGB)
        c2p = Photo2Cartoon()
        cartoon = c2p.inference(img)
        if cartoon is not None:
            cv2.imwrite("static/cartoon-test.jpg", cartoon)
            print('Cartoon portrait has been saved successfully!')
        return render_template("index.html",output=codehtml)

        #return render_template("index.html",output=htmloader(text,legoutput[1],fpath))
    #return xieon
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()