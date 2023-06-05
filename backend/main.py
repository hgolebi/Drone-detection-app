from flask import (
    Flask, flash, request, redirect, url_for, send_from_directory, render_template,
    abort, jsonify, send_file, after_this_request
)
from flask_cors import CORS
from werkzeug.utils import secure_filename
from backend import thumbnails
from MinioClient import MinioClient
from FileRemover import FileRemover
import http.client as client
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_login import (
    login_required, login_user, logout_user, current_user, LoginManager
)
from flask_bcrypt import Bcrypt
from models import db, User, Movie, MovieWithDetection
import time
import os


absolute_path = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = os.path.join(absolute_path, './tmp')
ALLOWED_EXTENSIONS = {'mp4', 'mov'}


minio_client = MinioClient("172.20.0.3:9000")
# minio_client.set_client('03')


file_remover = FileRemover()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tracking_system:password@172.20.0.4:5432/tracking_system'
app.config['SECRET_KEY'] = os.environ.get(
    'FLASK_SECRET_KEY', 'fallback_secret_key')
CORS(app, resources={r"/*": {'origins': '*'}}, supports_credentials=True, allow_headers='*')

db.init_app(app)
with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@app.post('/register')
def register_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'message': 'Missing user registration data'}), 400
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username is already taken'}), 400

    hash_pswd = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hash_pswd)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.post('/login')
def login_authenticate():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'message': 'Missing user login data'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': f'User not found'}), 404
    elif user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': f'Hello {current_user.username}'}), 200
    else:
        return jsonify({'message': f'Invalid password'}), 404


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logging out.'}), 200


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
@login_required
def upload_file():
    if request.method == 'GET':
        return jsonify([f'{i.name}' for i in Movie.query.filter_by(user_id = current_user.get_id()).all()])

    if request.method == 'POST':
        # check if the post request has the file part
        minio_client.set_client(current_user.get_id())
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

            if Movie.query.filter_by(name=filename).first() is not None:
                return jsonify({'message': f'A file with the name {filename} already exists'}), 400

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            minio_client.put_video(filename)

            extension = filename.rsplit('.', 1)[-1].lower()
            movie = Movie(name=filename, extension=extension,
                          user_id=current_user.get_id())
            db.session.add(movie)
            db.session.commit()

            # thumbnails.generate_thumbnail(filename)
            return jsonify({'message': 'Video upload.'}), 200

        return jsonify({'message': 'Video not upload.'}), 400


# @app.route('/video/')
# @login_required
# def show_videos():
#     videos = [i for i in minio_client.list_names()]
#     return jsonify(videos)


@app.route('/videos/<name>')
@login_required
def show_file(name):
    minio_client.set_client(current_user.get_id())
    as_attachment = 'attachment' in request.args
    fp = minio_client.get_video(name)
    resp = send_file(fp, download_name=name, as_attachment=as_attachment)
    file_remover.cleanup_once_done(resp, fp)
    return resp


@app.route('/thumbnails/<name>')
@login_required
def show_thumb(name):
    minio_client.set_client(current_user.get_id())
    fp = minio_client.get_thumbnail(name)
    resp = send_file(fp, download_name=thumbnails.thumbnail_name(name))
    file_remover.cleanup_once_done(resp, fp)
    return resp


@app.route('/tracked_videos/<name>')
@login_required
def get_tracked(name):

    threshold = request.args.get('treshold')
    tracker = request.args.get('tracker')
    if not threshold or not tracker:
        return jsonify({'message', 'Missing threshold or tracker parameter'}), 400

    threshold = float(threshold)
    name = name_norm2track(name, threshold, tracker)

    as_attachment = request.args.get('as_attachment')
    minio_client.set_client(current_user.get_id())
    fp = minio_client.get_tracked(name)
    resp = send_file(fp, download_name=name, as_attachment=as_attachment)
    file_remover.cleanup_once_done(resp, fp)
    return resp


@app.route('/tracking/<name>', methods=['POST'])
@login_required
def tracking(name):
    tracker = request.json.get('tracker')
    threshold = request.json.get('treshold')

    if not threshold or not tracker:
        return jsonify({'message': 'Missing treshold or tracker info'}, 400)

    threshold = float(threshold)

    minio_client.set_client(current_user.get_id())
    conn = client.HTTPConnection('172.20.0.5', 5000)
    conn.request(
        "GET", f"/{name}?user_id={current_user.get_id()}&threshold={threshold}&tracker={tracker}")
    response = conn.getresponse()

    if (response.status != 200):
        return jsonify({'message': 'Database bad response'}, 500)
    filename = name_norm2track(name, threshold, tracker)

    extension = filename.rsplit('.', 1)[-1].lower()
    # movie_with_detection = MovieWithDetection.query.join(
    #     MovieWithDetection.source_movie).filter(and_(Movie.user_id == current_user.get_id(), MovieWithDetection.name == filename)).all()
    # for i in movie_with_detection:
    #     db.session.delete(i)
    # db.session.delete(movie_with_detection)
    src_movie = Movie.query.filter(and_(Movie.user_id == current_user.get_id(), Movie.name == name)).first()
    movie_with_detection = MovieWithDetection(
        name=filename,
        extension=extension,
        source_movie_id=src_movie.movie_id,
    )
    db.session.add(movie_with_detection)
    db.session.commit()
    fp = minio_client.get_tracked(name_norm2track(name, threshold, tracker))
    resp = send_file(fp, download_name=name)
    file_remover.cleanup_once_done(resp, fp)
    return jsonify({'message': 'Tracked video generated'}), 201
