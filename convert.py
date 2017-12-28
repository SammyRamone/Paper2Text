import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/home/marc/upload_test'
ALLOWED_EXTENSIONS = set(['pdf'])
PATH_TO_K2PDF = "/home/marc/Downloads/k2pdfopt"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_file(filename):
    new_filename = filename.rsplit('.', 1)[0] + "k2opt.pdf"
    os.system(PATH_TO_K2PDF + " -x -o " + os.path.join(app.config['UPLOAD_FOLDER'], new_filename) + " " + os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #os.system("rm " + filename)
    return new_filename

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_filename = convert_file(file.filename)
            return redirect(url_for('uploaded_file',
                                    filename=new_filename))
    return '''
    <!doctype html>
    <title>Convert a File</title>
    <h1>Convert a File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    #todo delte file in upload folder