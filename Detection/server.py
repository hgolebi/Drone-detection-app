from minio import Minio
from minio.error import S3Error
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask import abort, jsonify, send_file, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from Detection import object_tracking
import subprocess
import os

app = Flask(__name__)
CORS(app, origins="*")

minio_client = Minio("172.20.0.3:9000", access_key="tracking_system",
                     secret_key="password", secure=False)


@app.route("/<name>")
def hello_word(name):

    if not "user_id" in request.args:
        abort(400)

    if not 'threshold' in request.args:
        abort(400)

    if not 'tracker' in request.args:
        abort(400)


    user_id = request.args['user_id']
    threshold = float(request.args['threshold'])
    tracker = (request.args['tracker'])
    found = minio_client.bucket_exists(f"user{user_id}")
    if not found:
        abort(400)

    minio_client.fget_object(
        f"user{user_id}", f"video/{name}", f"Detection/tmp/{name}")
    try:
        ot = object_tracking.ObjectTracking(name=tracker, threshold=threshold)
    except ValueError:
        abort(400)

    ot.get_video(f"Detection/tmp/{name}", f"Detection/tmp/out.mp4", )
    ot.run()

    command = f"ffmpeg -y -i Detection/tmp/out.mp4 -c:v libx264 -preset medium -crf 23 -c:a copy Detection/tmp/out_avc1.mp4"
    subprocess.call(command, shell=True)

    new_name = name[:name.rfind('.')]
    new_name = f'{new_name}-{int(threshold*10000)}-{tracker}.mp4'
    adnotations_name = new_name.replace('.mp4', '.txt')

    minio_client.fput_object(
        f"user{user_id}", f"tracked/{new_name}", f"Detection/tmp/out_avc1.mp4", content_type='video/mp4')

    minio_client.put_object(f"user{user_id}", f"adnotations/{adnotations_name}",
                            ot.get_adnotations(), length=-1, part_size=10485760)
    os.remove(f"Detection/tmp/out.mp4")
    os.remove(f"Detection/tmp/out_avc1.mp4")
    os.remove(f"Detection/tmp/{name}")
    return """<!doctype html>
        OK"""
