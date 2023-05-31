from minio import Minio
from minio.error import S3Error
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask import abort, jsonify, send_file, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from Detection import object_tracking
import os

app = Flask(__name__)
CORS(app, origins="*")

minio_client = Minio("localhost:9000", access_key="tracking_system",
                     secret_key="password", secure=False)


@app.route("/<name>")
def hello_word(name):
    if not "user_id" in request.args:
        abort(400)

    user_id = request.args['user_id']
    found = minio_client.bucket_exists(f"user{user_id}")
    if not found:
        abort(400)

    minio_client.fget_object(
        f"user{user_id}", f"video/{name}", f"Detection/tmp/{name}")

    ot = object_tracking.ObjectTracking()
    ot.get_video(f"Detection/tmp/{name}", f"Detection/tmp/out.mp4")
    ot.run()

    minio_client.fput_object(
        f"user{user_id}", f"tracked/{name}", f"Detection/tmp/out.mp4", content_type='video/mp4')

    os.remove("./Detecton/tmp/out.mp4")
    os.remove(f"./Detecton/tmp/{name}")
    return """<!doctype html>
        OK"""
