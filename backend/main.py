import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask import abort, jsonify, send_file, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from backend import thumbnails
from MinioClient import MinioClient
from FileRemover import FileRemover
import http.client as client
import time

absolute_path = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = os.path.join(absolute_path, './tmp')
ALLOWED_EXTENSIONS = {'mp4', 'mov'}


minio_client = MinioClient("172.20.0.3:9000")
minio_client.set_client('03')


file_remover = FileRemover()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, origins="*")


def name_norm2track(name, threshold, tracker):
    new_name = name[:name.rfind('.')]
    new_name = f'{name}-{int(threshold*10000)}-{tracker}.mp4'
    return new_name


@app.route("/")
def hello_word():
    title = "GRUPA ŚLEDCZA"
    videos = [i for i in minio_client.list_names()]

    return render_template(os.path.join(absolute_path, "templates", '/index.html'), title=title, videos=videos)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/videos', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        video_list = [i for i in minio_client.list_names()]
        return jsonify(video_list)

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
            minio_client.put_video(filename)
            # thumbnails.generate_thumbnail(filename)
            return redirect(url_for('hello_word'))


# @app.route('/video/')
# def show_videos():
#     videos = [i for i in minio_client.list_names()]
#     return jsonify(videos)


@app.route('/videos/<name>')
def show_file(name):
    as_attachment = 'attachment' in request.args
    fp = minio_client.get_video(name)
    resp = send_file(fp, download_name=name, as_attachment=as_attachment)
    file_remover.cleanup_once_done(resp, fp)
    return resp


@app.route('/thumbnails/<name>')
def show_thumb(name):
    fp = minio_client.get_thumbnail(name)
    resp = send_file(fp, download_name=thumbnails.thumbnail_name(name))
    file_remover.cleanup_once_done(resp, fp)
    return resp


@app.route('/tracked_videos/<name>')
def get_tracked(name):
    if ('threshold' in request.args) ^ ('tracker' in request.args):
        abort(400)

    if ('threshold' in request.args) and ('tracker' in request.args):
        threshold = float(request.args['threshold'])
        tracker = (request.args['tracker'])
        name = name_norm2track(name, threshold, tracker)

    as_attachment = 'attachment' in request.args
    fp = minio_client.get_tracked(name)
    resp = send_file(fp, download_name=name, as_attachment=as_attachment)
    file_remover.cleanup_once_done(resp, fp)
    return resp


@app.route('/processed_videos/<name>')
def tracking(name):

    if not 'threshold' in request.args:
        abort(400)

    if not 'tracker' in request.args:
        abort(400)

    threshold = float(request.args['threshold'])
    tracker = (request.args['tracker'])

    conn = client.HTTPConnection('172.20.0.5', 5000)
    conn.request(
        "GET", f"/{name}?user_id={minio_client.get_clent()[-2:]}&threshold={threshold}&tracker={tracker}")
    response = conn.getresponse()

    if (response.status != 200):
        abort(response.status)

    fp = minio_client.get_tracked(name_norm2track(name, threshold, tracker))
    resp = send_file(fp, download_name=name)
    file_remover.cleanup_once_done(resp, fp)
    return resp
