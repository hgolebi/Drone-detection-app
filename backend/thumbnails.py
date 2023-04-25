import os
import subprocess
import cv2

absolute_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(absolute_path, './uploads')
THUMBNAIL_FOLDER = os.path.join(absolute_path, './thumbnails')


def thumbnail_name(videoname: str):
    return "_".join(videoname.split('.'))+".png"


def generate_thumbnail(videoname: str, size=500):
    thumb_name = thumbnail_name(videoname)
    # cmd = ['ffmpeg', '-y', '-i', f'{UPLOAD_FOLDER}/{videoname}', '-vf', f'thumbnail=n={n}',
    #        '-frames:v', '1', f'{THUMBNAIL_FOLDER}/{thumb_name}', '-loglevel', 'quiet']
    # subprocess.run(cmd, shell=False)
    video = cv2.VideoCapture(UPLOAD_FOLDER + videoname)
    success, image = video.read()
    if not success:
        return False
    width = image.shape[1]
    height = image.shape[0]
    scale_percent = max(height / size, width / size)
    dim = (int(width / scale_percent), int(height / scale_percent))
    thumbnail = cv2.resize(image, dim)

    cv2.imwrite(THUMBNAIL_FOLDER + thumb_name, thumbnail)
    video.release()


def check_thumbnail(videname: str):
    thumb_name = thumbnail_name(videname)
    if not thumb_name in os.listdir(THUMBNAIL_FOLDER):
        generate_thumbnail(videname, 100)


# check_thumbnail("film.mp4")
