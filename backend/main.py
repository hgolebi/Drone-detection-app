import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask import abort, jsonify
from werkzeug.utils import secure_filename
import thumbnails

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def hello_word():
    title = "GRUPA ŚLEDCZA"
    videos = os.listdir("./uploads/")
    videos = [v for v in videos if v.endswith(tuple(ALLOWED_EXTENSIONS))]

    return render_template('./index.html', title=title, videos=videos)
# """<p>hello world</p>
#     <a href=./upload/> Dodaj wideo </a>
#     """


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            thumbnails.generate_thumbnail(filename)
            return redirect(url_for('hello_word'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/video/')
def show_videos():
    video_list = os.listdir(app.config["UPLOAD_FOLDER"])
    video_list = [v for v in video_list if v.endswith(
        tuple(ALLOWED_EXTENSIONS))]
    return jsonify(video_list)


@app.route('/video/<name>')
def show_file(name):
    as_attachment = 'attachment' in request.args

    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=as_attachment)


@app.route('/thumbnail/<name>')
def show_thumb(name):
    if not name in os.listdir(app.config["UPLOAD_FOLDER"]):
        abort(404)
    thumb_name = thumbnails.thumbnail_name(name)
    thumbnails.check_thumbnail(name)
    return send_from_directory('./thumbnails', thumb_name)
# @app.route('/download/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)
