import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask import abort, jsonify, send_file, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from backend import thumbnails
from MinioClient import MinioClient
from FileRemover import FileRemover


# from Detection import object_tracking
import time

absolute_path = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = os.path.join(absolute_path, './uploads')
ALLOWED_EXTENSIONS = {'mp4', 'mov'}


minio_client = MinioClient("172.20.0.3:9000")
minio_client.set_client('03')


file_remover = FileRemover()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, origins="*")


@app.route("/")
def hello_word():
    title = "GRUPA ŚLEDCZA"
    videos = [i for i in minio_client.list_names()]
    # videos = [v for v in videos if v.endswith(tuple(ALLOWED_EXTENSIONS))]

    return render_template(os.path.join(absolute_path, "templates", '/index.html'), title=title, videos=videos)
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
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            minio_client.put_object(filename, file)
            # thumbnails.generate_thumbnail(filename)
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
    videos = [i for i in minio_client.list_names()]
    return jsonify(videos)


@app.route('/video/<name>')
def show_file(name):
    as_attachment = 'attachment' in request.args
    fp = minio_client.get_object(name)
    resp = send_file(fp, download_name=name, as_attachment=as_attachment)
    file_remover.cleanup_once_done(resp, fp)
    return resp

    # @app.after_this_response
    # def delete(response):
    #     os.remove(f"./tmp/{name}")
    #     return response

    # return send_from_directory("./tmp/", name, as_attachment=as_attachment)


@app.route('/thumbnail/<name>')
def show_thumb(name):
    if not name in os.listdir(app.config["UPLOAD_FOLDER"]):
        abort(404)
    thumb_name = thumbnails.thumbnail_name(name)
    thumbnails.check_thumbnail(name)
    return send_from_directory('./thumbnails', thumb_name)


# @app.route('/tracking/<name>')
# def run_yolo(name):
#     if not name in os.listdir(app.config["UPLOAD_FOLDER"]):
#         abort(404)
#     out_name = f"out_{name}"
#     ot = object_tracking.ObjectTracking()
#     ot.get_video(os.path.join(app.config["UPLOAD_FOLDER"], name),
#                  os.path.join(absolute_path, "tracked", out_name))
#     ot.run()

#     return send_from_directory(app.config["UPLOAD_FOLDER"], out_name, as_attachment=True)

# @app.route('/download/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)
