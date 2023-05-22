import os
import subprocess

UPLOAD_FOLDER = './uploads'
THUMBNAIL_FOLDER = './thumbnails'


def thumbnail_name(videoname: str):
    return "_".join(videoname.split('.'))+".png"


def generate_thumbnail(videoname: str, n=500):
    thumb_name = thumbnail_name(videoname)
    cmd = ['ffmpeg', '-y', '-i', f'{UPLOAD_FOLDER}/{videoname}', '-vf', f'thumbnail=n={n}',
           '-frames:v', '1', f'{THUMBNAIL_FOLDER}/{thumb_name}', '-loglevel', 'quiet']
    subprocess.run(cmd, shell=False)


def check_thumbnail(videname: str):
    thumb_name = thumbnail_name(videname)
    if not thumb_name in os.listdir(THUMBNAIL_FOLDER):
        generate_thumbnail(videname, 100)


check_thumbnail("film.mp4")
