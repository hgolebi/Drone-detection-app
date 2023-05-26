import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask import abort, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import thumbnails
from Detection import object_tracking
import time

absolute_path = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = os.path.join(absolute_path, './uploads')
TRACKED_FOLDER = os.path.join(absolute_path, './tracked')

ALLOWED_EXTENSIONS = {'mp4', 'mov'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRACKED_FOLDER'] = TRACKED_FOLDER
CORS(app)


@app.route("/")
def hello_word():
    title = "GRUPA ŚLEDCZA"
    videos = os.listdir(os.path.join(absolute_path, "./uploads/"))
    videos = [v for v in videos if v.endswith(tuple(ALLOWED_EXTENSIONS))]
    return render_template('index.html', title=title, videos=videos)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/videos', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        video_list = os.listdir(app.config["UPLOAD_FOLDER"])
        video_list = [v for v in video_list if v.endswith(
            tuple(ALLOWED_EXTENSIONS))]
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
            thumbnails.generate_thumbnail(filename)
            return redirect(url_for('hello_word'))


@app.route('/videos/<name>')
def show_file(name):
    as_attachment = 'attachment' in request.args
    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=as_attachment)


@app.route('/thumbnails/<name>')
def show_thumb(name):
    if not name in os.listdir(app.config["UPLOAD_FOLDER"]):
        abort(404)
    thumb_name = thumbnails.thumbnail_name(name)
    thumbnails.check_thumbnail(name)
    return send_from_directory('./thumbnails', thumb_name)


@app.route('/processed_videos/<name>')
def run_yolo(name):
    if_att = 'attachment' in request.args
    out_name = f"out_{name}"
    if not out_name in os.listdir(app.config['TRACKED_FOLDER']):
        if not name in os.listdir(app.config["UPLOAD_FOLDER"]):
            abort(404)
        ot = object_tracking.ObjectTracking()
        ot.get_video(os.path.join(app.config["UPLOAD_FOLDER"], name),
                    os.path.join(absolute_path, "tracked", out_name))
        ot.run()
    return send_from_directory(app.config["TRACKED_FOLDER"], out_name, as_attachment=if_att)


if __name__ == '__main__':
    app.run(debug=True)