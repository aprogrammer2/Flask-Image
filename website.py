import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import random

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '143249191357631105'



@app.route("/",methods=['GET','POST'])
def show_pics():
    content = random.choice(os.listdir("static"))
    imagepath = 'static/' + content
    content2 = content
    while content2 == content:
        content2 = random.choice(os.listdir("static"))
    description2 = content2.split('.')[0]
    description1 = content.split('.')[0]
    image2path = 'static/' + content2
    return render_template('index.html',imagepath=imagepath, image2path=image2path, description1=description1,description2=description2)
def send_filter():
    return '<script>window.location = "/filter/'+ tag + ';</script>"'
@app.route("/filter/<tag>",methods=['POST','GET'])
def filter(tag):
    matches = []
    for description in os.listdir('static'):
        print(description)
        if tag in description:
            matches.append(description)
    print(description)
    try:
        content = random.choice(matches)
    except IndexError:
        return '<script>alert("No Results :("); \n window.location="/"</script>'
    
    imagepath = '/static/' + content
    content2 = content
    attempts = 0
    while content2 == content and attempts != 5:
        try:
            content2 = random.choice(matches)
        except:
            return '<script>alert("No Results :("); \n window.location="/"</script>'
        attempts += 1
    image2path = '/static/' + content2
    description2 = content2.split('.')[0]
    description1 = content.split('.')[0]
    return render_template('index.html',imagepath=imagepath, image2path=image2path, description1=description1,description2=description2)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/new', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        description = request.form['description']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            extension = file.filename.split('.')[len(file.filename.split('.'))-1]
            filename = description + '.' + extension
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload New Picture</title>
    <h1>Upload New Picture</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
      <input type=string name=description>
    </form>
    '''
app.run(host='192.168.1.7')
