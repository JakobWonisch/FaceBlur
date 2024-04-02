from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import io
import json
from detect import detect
from process_folder import setup_opts

UPLOAD_FOLDER = './workspace'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg' }

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_file("config.json", load=json.load)

@app.route("/")
def hello_world():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/blur-please', methods=['POST'])
def blur():
    if 'file' not in request.files:
        return "no file part", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "no file selected", 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        opt = setup_opts(app.config['UPLOAD_FOLDER'], filename)

        try:
            detect(opt)
        except Exception as error:
            return "could not process image", 500

        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], "output", filename),
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='image.jpeg'
        )